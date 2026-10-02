import json
import os

from openai import OpenAI

from .skills import load_skill, load_skills_signature
from .tools import SCHEMAS, TOOLS

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")


def agent_loop(content: str):
    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    skills_map, skills_signature = load_skills_signature(
        ".claude/skills/"
    )  # will only works for linux and macos but since it only test for linux will not change it for now
    messages = []
    if skills_signature:
        messages.append({"role": "system", "content": skills_signature})

    if content.startswith("/"):
        skills, skill_args = parse_skills(content, skills_map)
        if skills:
            for skill in skills:
                skill_content = load_skill(skills_map[skill], skill, skill_args)
                messages.append({"role": "user", "content": skill_content})
        else:
            messages.append({"role": "user", "content": content})
    else:
        messages.append({"role": "user", "content": content})

    import sys

    # print(f"message before tool calling: {messages}", file=sys.stderr)
    while True:
        chat = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            messages=messages,
            tools=SCHEMAS,
        )
        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        messages.append(chat.choices[0].message)

        # You can use print statements as follows for debugging, they'll be visible when running tests.
        # print("Logs from your program will appear here!", file=sys.stderr)

        if chat.choices[0].message.tool_calls:
            print(
                f"message from tool calling: {chat.choices[0].message}", file=sys.stderr
            )
            for msg in execute_tool_calls(chat.choices[0].message.tool_calls):
                messages.append(msg)
        else:
            print(chat.choices[0].message.content)
            break


def execute_tool_calls(tool_calls):
    for tool_call in tool_calls:
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        tool = TOOLS[func_name]
        content = tool.execute(**args)
        yield {"role": "tool", "tool_call_id": tool_call.id, "content": content}


def parse_skills(prompt: str, skills_map):
    tokens = prompt.strip().split()
    skill_cnt = 0
    for token in tokens:
        if token.startswith("/") and token[1:] in skills_map:
            skill_cnt += 1
        else:
            break
    skills = [token[1:] for token in tokens[:skill_cnt]]
    args = tokens[skill_cnt:]

    return skills, args
