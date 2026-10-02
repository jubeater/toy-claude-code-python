from ..skills import load_skill

SCHEMA = {
    "type": "function",
    "function": {
        "name": "Skill",
        "description": "Load a skill's instructions into the conversation",
        "parameters": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the skill to use",
                },
                "args": {
                    "type": "string",
                    "description": "Optional arguments for the skill",
                },
            },
        },
    },
}


def execute(name: str, args: str, skills_map) -> str:
    try:
        args_list = args.strip().split()
        content = load_skill(skills_map[name], name, args_list)
        return content
    except Exception as e:  # noqa: BLE001
        return str(e)
