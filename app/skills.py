import sys
from pathlib import Path


def load_skills_signature(folder_path: str):
    folder = Path(folder_path)
    skills_signature = "You have access to the following skills:\n\n"
    skill_map = {}
    for f in folder.iterdir():
        inside_delimiter = False
        skill_path = f / "SKILL.md"
        if skill_path.exists() and skill_path.is_file():
            print(f"--- Reading Skill: {skill_path.name} ---", file=sys.stderr)
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
                        if clean_line.startswith("name: "):
                            name = clean_line.partition("name:")[2]
                        elif clean_line.startswith("description:"):
                            description = clean_line.partition("description:")[2]
            print(f"--- Save skill of name: {name} ---", file=sys.stderr)
            skills_signature += f"- {name}: {description}"
            skill_map[name] = skill_path

    return skill_map, skills_signature


def load_skill(skill_path: Path):
    if skill_path.exists() and skill_path.is_file():
        print(f"--- Loading Skill Content: {skill_path.name} ---", file=sys.stderr)
        delimiter_cnt = 0
        contents = ""
        with skill_path.open(encoding="utf-8") as file:
            for line in file:
                if delimiter_cnt < 2 and line.strip() == "---":
                    delimiter_cnt += 1
                elif delimiter_cnt == 2:
                    contents += line
        return contents
