from . import bash, read, write

TOOLS = {
    "Read": read,
    "Write": write,
    "Bash": bash,
}

SCHEMAS = [tool.SCHEMA for tool in TOOLS.values()]
