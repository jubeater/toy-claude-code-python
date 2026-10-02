import subprocess

SCHEMA = {
    "type": "function",
    "function": {
        "name": "Bash",
        "description": "Execute a shell command",
        "parameters": {
            "type": "object",
            "required": ["command"],
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The command to execute",
                }
            },
        },
    },
}


def execute(command: str) -> str:

    result = subprocess.run(
        ["bash", "-lc", command], capture_output=True, text=True, check=False
    )
    if result.returncode == 0:
        return result.stdout
    else:
        return result.stderr
