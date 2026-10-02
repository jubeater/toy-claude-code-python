import argparse
import os
import sys
import json
from pathlib import Path
from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    read_tool = {
        "type": "function",
        "function": {
            "name": "Read",
            "description": "Read and return the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read",
                    }
                },
                "required": ["file_path"],
            },
        },
    }
    messages = [{"role": "user", "content": args.p}]
    tools = [read_tool]

    chat = client.chat.completions.create(
        model="anthropic/claude-haiku-4.5",
        messages=messages,
        tools=tools,
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")

    while True:
        messages.append(chat.choices[0].message)
        # You can use print statements as follows for debugging, they'll be visible when running tests.
        # print("Logs from your program will appear here!", file=sys.stderr)

        if chat.choices[0].message.tool_calls:
            result_gen = execute_tool_calls(chat.choices[0].message.tool_calls)
            messages.extend(result_gen)
        else:
            print(chat.choices[0].message.content)
            break


def execute_tool_calls(tool_calls):
    for tool_call in tool_calls:
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        if func_name == "Read":
            file_path = args["file_path"]
            contents = Path(file_path).read_text(encoding="utf-8")
            yield {"role": "tool", "tool_call_id": tool_call.id, "content": contents}


if __name__ == "__main__":
    main()
