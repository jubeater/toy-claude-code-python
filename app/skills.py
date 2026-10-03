import re
from pathlib import Path


def load_skills_signature(folder_path: str):
    folder = Path(folder_path)
    if not folder.is_dir():
        return {}, ""
    skills_signature = "You have access to the following skills:\n\n"
    skill_map = {}
    for f in folder.iterdir():
        inside_delimiter = False
        skill_path = f / "SKILL.md"
        if skill_path.exists() and skill_path.is_file():
            # print(f"--- Reading Skill: {skill_path.name} ---", file=sys.stderr)
            name = ""
            description = ""

            with skill_path.open(encoding="utf-8") as file:
                for line in file:
                    clean_line = line.strip()
                    if clean_line == "---":
                        if inside_delimiter:
                            inside_delimiter = False
                            break
                        else:
                            inside_delimiter = True
                            continue
                    if inside_delimiter:
                        if clean_line.startswith("name:"):
                            name = clean_line.partition("name:")[2].strip()
                        elif clean_line.startswith("description:"):
                            description = clean_line.partition("description:")[
                                2
                            ].strip()
            # print(f"--- Save skill of name: {name} ---", file=sys.stderr)
            skills_signature += f"- {name}: {description}\n\n"
            if not name:
                continue
            skill_map[name] = skill_path
    skills_signature += "If a skill matches the user's request, call the Skill tool with its name and follow the instructions it returns.\n"
    return skill_map, skills_signature


def load_skill(
    skill_path: Path, skill_name: str, skill_args: list[str]
) -> tuple[str, bool]:
    pattern_all = r"\$ARGUMENTS"
    pattern_single = r"\$ARGUMENTS\[(\d+)\]"
    pattern_short = r"\$(\d+)"
    fork_marker = "context: fork"
    all_args = " ".join(skill_args).strip()
    # print(f"--- prepare skill args: {skill_args} ---", file=sys.stderr)
    if skill_path.exists() and skill_path.is_file():
        # print(f"--- Loading Skill Content: {skill_path.name} ---", file=sys.stderr)
        delimiter_cnt = 0
        contents = ""
        using_fork = False
        with skill_path.open(encoding="utf-8") as file:
            for line in file:
                if delimiter_cnt < 2 and line.strip() == "---":
                    delimiter_cnt += 1
                elif delimiter_cnt < 2 and line.strip() == fork_marker:
                    using_fork = True
                elif delimiter_cnt == 2:
                    line = re.sub(
                        pattern_single,
                        lambda match: get_arg(match, skill_args),
                        line,
                    )
                    line = re.sub(
                        pattern_short,
                        lambda match: get_arg(match, skill_args),
                        line,
                    )
                    line = re.sub(pattern_all, all_args, line)
                    # print(
                    #     f"--- get final skill description: {line} ---", file=sys.stderr
                    # )
                    contents += line
        return contents, using_fork
    return f"Skill {skill_name} not found!", False


def get_arg(match: re.Match[str], skill_args: list[str]) -> str:
    index = int(match.group(1))
    return skill_args[index] if index < len(skill_args) else ""
