import sys
from pathlib import Path


def load_skills_signature(folder_path: str):
    folder = Path(folder_path)
    skills_signature = "You have access to the following skills:\n\n"
    inside_delimiter = False
    for f in folder.iterdir():
        if f.is_file() and f.name.endswith(".md"):
            print(f"--- Reading Skill: {f.name} ---", file=sys.stderr)
            name = ""
            description = ""

            with f.open(encoding="utf-8") as file:
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

            skills_signature += f"- {name}: {description}"

    return skills_signature
