from pathlib import Path

ROOT = Path(".")
pub_dir = ROOT / "content" / "publication"

REQUIRED_FIELDS = [
    'abstract',
    'url_dataset',
    'url_pdf',
    'url_project',
    'url_slides',
    'url_video',
]

for file_path in pub_dir.glob("*.md"):
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    in_frontmatter = False
    front_start = None
    front_end = None

    # find front matter block between +++ ... +++
    for i, line in enumerate(lines):
        if line.strip() == "+++":
            if not in_frontmatter:
                in_frontmatter = True
                front_start = i
            else:
                front_end = i
                break

    if front_start is None or front_end is None:
        # no TOML front matter; skip
        continue

    front_lines = lines[front_start:front_end+1]
    body_lines = lines[front_end+1:]

    # check which fields already exist
    present = {field: False for field in REQUIRED_FIELDS}
    for line in front_lines:
        stripped = line.strip()
        for field in REQUIRED_FIELDS:
            if stripped.startswith(field + " "):  # e.g. 'url_pdf = "..."'
                present[field] = True

    # if all fields already there, skip file
    if all(present.values()):
        continue

    # find insertion point: before first [[authors]] or before closing +++
    insert_index = None
    for i, line in enumerate(front_lines):
        if line.lstrip().startswith("[[authors]]"):
            insert_index = i
            break
    if insert_index is None:
        # no authors yet; insert before last +++
        insert_index = len(front_lines) - 1

    # build new field lines (only for missing fields)
    new_field_lines = []
    indent = ""  # no extra indent for key-value lines

    if not present["abstract"]:
        new_field_lines.append(f'{indent}abstract = ""\n')

    for field in REQUIRED_FIELDS[1:]:  # skip abstract, already handled
        if not present[field]:
            new_field_lines.append(f'{indent}{field} = ""\n')

    # insert new fields
    updated_front = (
        front_lines[:insert_index] +
        new_field_lines +
        front_lines[insert_index:]
    )

    # join everything back together
    new_text = "".join(updated_front + body_lines)
    file_path.write_text(new_text, encoding="utf-8")
    print(f"Updated template fields in {file_path}")
