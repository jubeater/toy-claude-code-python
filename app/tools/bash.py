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
    try:
        result = subprocess.run(
            ["bash", "-lc", command], capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr
    except Exception as e:  # noqa: BLE001
        return str(e)
