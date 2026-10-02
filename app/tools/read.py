from pathlib import Path

SCHEMA = {
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


def execute(file_path: str) -> str:
    try:
        content = Path(file_path).read_text(encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        content = str(e)
    return content
