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


def execute(name: str, skills_map, args: str = "") -> str:
    try:
        args_list = args.strip().split()
        content = load_skill(skills_map[name], name, args_list)
        return f"Skill: {name} (located at {skills_map[name].parent})\n{content}"
    except Exception as e:  # noqa: BLE001
        return str(e)
