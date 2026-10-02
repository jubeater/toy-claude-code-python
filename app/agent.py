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
    real_content = content
    if content.startswith("/"):
        skill_name = content.strip().partition("/")[2]
        real_content = load_skill(skills_map[skill_name])
    messages = [
        {"role": "system", "content": skills_signature},
        {"role": "user", "content": real_content},
    ]
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
