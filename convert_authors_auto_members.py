from pathlib import Path
import ast
import re

ROOT = Path(".")

# ========= CONFIGURE THESE LINES =========
# Directories that contain one .md file per person:
MEMBER_DIRS = [
    ROOT / "content" / "member",
    ROOT / "content" / "auditor",
    ROOT / "content" / "alumni",
    ROOT / "content" / "intern",
]

# Front matter fields that may contain the full name:
# e.g. name = "Full Name" or title = "Full Name"
MEMBER_NAME_FIELDS = ["name"]
# ============================================

def load_lab_members():
    """
    Scan all MEMBER_DIRS for Markdown files and extract member names
    from front matter fields (MEMBER_NAME_FIELDS).
    Returns a set of lowercase names.
    """
    lab_members = set()

    for members_dir in MEMBER_DIRS:
        if not members_dir.exists():
            # Skip directories that don't exist
            continue

        for md_file in members_dir.glob("*.md"):
            text = md_file.read_text(encoding="utf-8")
            lines = text.splitlines()

            in_frontmatter = False
            for line in lines:
                stripped = line.strip()

                # track TOML front matter delimiters +++
                if stripped == "+++":
                    in_frontmatter = not in_frontmatter
                    continue

                if not in_frontmatter:
                    continue

                # try to match e.g. name = "Full Name" or title = "Full Name"
                for field in MEMBER_NAME_FIELDS:
                    pattern = rf'^{field}\s*=\s*"(.*)"\s*$'
                    m = re.match(pattern, stripped)
                    if m:
                        name = m.group(1).strip()
                        if name:
                            lab_members.add(name.lower())
                            # assume one main name per file; go to next file
                            break
                else:
                    # inner loop not broken
                    continue
                # inner loop was broken (name found) -> break outer loop over lines
                break

    print(f"Loaded {len(lab_members)} lab members from {len(MEMBER_DIRS)} directories")
    return lab_members


LAB_MEMBERS = load_lab_members()

def is_lab_member(author_name: str) -> bool:
    """
    True if this author should be marked as a lab member.
    Matching is by full name (case-insensitive).
    """
    name_norm = author_name.strip().lower()
    return name_norm in LAB_MEMBERS


pub_dir = ROOT / "content" / "publication"

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
            # Example: authors = ["A, B", "C, D"]
            rhs = line.split("=", 1)[1].strip()

            try:
                authors_list = ast.literal_eval(rhs)
            except Exception:
                # If we can't parse it, keep original line
                new_lines.append(line)
                continue

            if not isinstance(authors_list, (list, tuple)):
                new_lines.append(line)
                continue

            # Preserve indentation of the original line
            indent = line[:len(line) - len(line.lstrip())]

            # Build [[authors]] blocks with is_member flag
            for author in authors_list:
                author = str(author)
                member_flag = "true" if is_lab_member(author) else "false"

                new_lines.append(f'{indent}[[authors]]\n')
                new_lines.append(f'{indent}name = "{author}"\n')
                new_lines.append(f'{indent}is_member = {member_flag}\n')
                new_lines.append('\n')

            changed = True
            continue  # don't keep original authors = [...] line

        new_lines.append(line)

    if changed:
        file_path.write_text("".join(new_lines), encoding="utf-8")
        print(f"Converted authors in {file_path}")
