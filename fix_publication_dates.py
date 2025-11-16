from pathlib import Path
import re

ROOT = Path(".")
pub_dir = ROOT / "content" / "publication"

for file_path in pub_dir.glob("*.md"):
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Find TOML front matter boundaries +++
    in_frontmatter = False
    front_start = None
    front_end = None

    for i, line in enumerate(lines):
        if line.strip() == "+++":
            if not in_frontmatter:
                in_frontmatter = True
                front_start = i
            else:
                front_end = i
                break

    if front_start is None or front_end is None:
        continue  # no valid front matter

    front_lines = lines[front_start:front_end + 1]
    body_lines = lines[front_end + 1:]

    has_date = False
    year_value = None

    for line in front_lines:
        stripped = line.strip()

        # Check for existing date
        if stripped.startswith("date "):
            has_date = True

        # Extract year = "YYYY"
        m = re.match(r'^year\s*=\s*"(.*)"\s*$', stripped)
        if m:
            year_value = m.group(1).strip()

    # If there's already a date or no year, skip
    if has_date or not year_value:
        continue

    # Build new front matter with a date line inserted after year
    new_front = []
    inserted = False
    for line in front_lines:
        new_front.append(line)
        if (not inserted) and line.strip().startswith("year "):
            new_front.append(f'date = "{year_value}-01-01"\n')
            inserted = True

    # If we didn't find a year line (shouldn't happen here), insert before closing +++
    if not inserted:
        new_front = front_lines[:-1] + [f'date = "{year_value}-01-01"\n'] + [front_lines[-1]]

    file_path.write_text("".join(new_front + body_lines), encoding="utf-8")
    print(f"Set date = \"{year_value}-01-01\" for {file_path}")
