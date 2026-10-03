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


def execute(name: str, skills_map, run_subagent, args: str = "") -> str:
    try:
        skill_path = skills_map[name]["path"]
        args_list = args.strip().split()
        body = load_skill(
            skill_path,
            name,
            args_list,
        )
        # however you expose context from frontmatter
        if skills_map[name]["using_fork"]:
            answer = run_subagent(body)
            return f"Skill {name} ran in a separate context and returned: {answer}"

        return f"Skill: {name} (located at {skills_map[name].parent})\n{body}"
    except Exception as e:  # noqa: BLE001
        return str(e)
