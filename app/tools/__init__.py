from . import bash, read, skill, write

TOOLS = {
    "Read": read,
    "Write": write,
    "Bash": bash,
    "Skill": skill,
}

SCHEMAS = [tool.SCHEMA for tool in TOOLS.values()]
