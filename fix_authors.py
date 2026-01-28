from pathlib import Path
import ast

pub_dir = Path("content/publication")

for file_path in pub_dir.glob("*.md"):
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Skip files that already use [[authors]] syntax
    if any(l.lstrip().startswith("[[authors]]") for l in lines):
        continue

    new_lines = []
    changed = False
    in_frontmatter = False

    for line in lines:
        stripped = line.strip()

        # Track TOML front matter boundaries +++
        if stripped == "+++":
            in_frontmatter = not in_frontmatter
            new_lines.append(line)
            continue

        if in_frontmatter and stripped.startswith("authors ="):
            # Example line: authors = ["A, B", "C, D"]
            rhs = line.split("=", 1)[1].strip()

            try:
                authors_list = ast.literal_eval(rhs)
            except Exception:
                # If we can't parse it, just keep the original line
                new_lines.append(line)
                continue

            if not isinstance(authors_list, (list, tuple)):
                new_lines.append(line)
                continue

            # Preserve indentation of the original line
            indent = line[:len(line) - len(line.lstrip())]

            # Build [[authors]] blocks
            for author in authors_list:
                author = str(author)
                new_lines.append(f'{indent}[[authors]]\n')
                new_lines.append(f'{indent}name = "{author}"\n')
                # If you want to default is_member:
                # new_lines.append(f'{indent}is_member = false\n')
                new_lines.append('\n')

            changed = True
            continue  # do not keep the original authors = [...] line

        new_lines.append(line)

    if changed:
        file_path.write_text("".join(new_lines), encoding="utf-8")
        print(f"Converted authors in {file_path}")
