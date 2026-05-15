from pathlib import Path
import re
import unicodedata

import bibtexparser

ROOT = Path(".")

# Where your BibTeX is
BIB_PATH = ROOT / "publications.bib"

# Directories that contain one .md file per person (lab members, auditors, alumni, interns)
MEMBER_DIRS = [
    ROOT / "content" / "member",
    ROOT / "content" / "auditor",
    ROOT / "content" / "alumni",
    ROOT / "content" / "intern",
]

# Front matter fields in those files that contain the full name
MEMBER_NAME_FIELDS = ["name"]  # you said you use only "name"


def normalize_title(s: str) -> str:
    """Normalize titles for matching: lowercase, strip accents, remove punctuation."""
    s = s or ""
    s = s.lower()
    s = s.replace("{", "").replace("}", "")  # remove BibTeX braces
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\s]", "", s)
    return s.strip()


def toml_escape(s: str) -> str:
    """Escape string for use in TOML double-quoted string."""
    if s is None:
        return ""
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_bib_date(date_str: str):
    """
    Parse a BibTeX date string like '2023-04-15' or '2023-04' or '2023'
    into (year, month, day). Month/day default to '01' if missing.
    Returns (None, None, None) if it can't parse a year.
    """
    if not date_str:
        return None, None, None
    s = date_str.strip().strip("{}\"'")
    m = re.match(r"(\d{4})(?:-(\d{1,2})(?:-(\d{1,2}))?)?", s)
    if not m:
        return None, None, None
    year = m.group(1)
    month = m.group(2) or "1"
    day = m.group(3) or "1"
    # zero-pad
    month = f"{int(month):02d}"
    day = f"{int(day):02d}"
    return year, month, day


def load_lab_members():
    """Scan MEMBER_DIRS for Markdown files and extract member names from MEMBER_NAME_FIELDS."""
    lab_members = set()

    for members_dir in MEMBER_DIRS:
        if not members_dir.exists():
            continue

        for md_file in members_dir.glob("*.md"):
            text = md_file.read_text(encoding="utf-8")
            lines = text.splitlines()

            in_frontmatter = False
            for line in lines:
                stripped = line.strip()

                if stripped == "+++":
                    in_frontmatter = not in_frontmatter
                    continue

                if not in_frontmatter:
                    continue

                for field in MEMBER_NAME_FIELDS:
                    pattern = rf'^{field}\s*=\s*"(.*)"\s*$'
                    m = re.match(pattern, stripped)
                    if m:
                        name = m.group(1).strip()
                        if name:
                            lab_members.add(name.lower())
                            break
                else:
                    continue
                break

    print(f"Loaded {len(lab_members)} lab members from {len(MEMBER_DIRS)} directories")
    return lab_members


LAB_MEMBERS = load_lab_members()


def is_lab_member(author_name: str) -> bool:
    """
    Check if author is a lab member.
    Match on first+last name, ignoring order (e.g. 'Last, First' vs 'First Last').
    """

    def split_name(s: str):
        s = (s or "").lower().strip()
        # remove periods and extra punctuation except comma & space
        s = re.sub(r"[^\w\s,]", "", s)
        # if format 'Last, First'
        if "," in s:
            last_part, first_part = [p.strip() for p in s.split(",", 1)]
            last_tokens = last_part.split()
            first_tokens = first_part.split()
        else:
            parts = s.split()
            if not parts:
                return "", ""
            # format 'First [Middle] Last'
            first_tokens = parts[:-1]
            last_tokens = parts[-1:]
        first = first_tokens[0] if first_tokens else ""
        last = last_tokens[-1] if last_tokens else ""
        return first, last

    a_first, a_last = split_name(author_name)
    if not a_last:
        return False

    for member_name in LAB_MEMBERS:
        m_first, m_last = split_name(member_name)
        if not m_last:
            continue

        # Last name must match
        if a_last != m_last:
            continue

        # If we have a first name on both sides, require match too
        if a_first and m_first and a_first != m_first:
            continue

        # Good enough match
        return True

    return False


def load_bib_entries():
    if not BIB_PATH.exists():
        raise FileNotFoundError(f"BibTeX file not found: {BIB_PATH}")

    with BIB_PATH.open("r", encoding="utf-8") as f:
        bib_db = bibtexparser.load(f)

    entries_by_title = {}
    for entry in bib_db.entries:
        title = entry.get("title", "")
        norm = normalize_title(title)
        if norm:
            entries_by_title[norm] = entry

    print(f"Loaded {len(entries_by_title)} BibTeX entries from {BIB_PATH}")
    return entries_by_title


BIB_ENTRIES_BY_TITLE = load_bib_entries()

pub_dir = ROOT / "content" / "publication"

for file_path in pub_dir.glob("*.md"):

    # Skip danger.md entirely
    if file_path.name == "danger.md":
        continue

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
        # no valid front matter
        continue

    front_lines = lines[front_start:front_end + 1]
    body_lines = lines[front_end + 1:]

    # Extract title from front matter
    title = None
    for line in front_lines:
        stripped = line.strip()
        m = re.match(r'^title\s*=\s*"(.*)"\s*$', stripped)
        if m:
            title = m.group(1).strip()
            break

    if not title:
        print(f"[WARN] No title found in {file_path}, skipping")
        continue

    norm_title = normalize_title(title)
    entry = BIB_ENTRIES_BY_TITLE.get(norm_title)

    if not entry:
        print(f"[WARN] No matching BibTeX entry for title in {file_path}")
        continue

    # --- Get data from BibTeX entry ---
    bib_title = entry.get("title", title)
    bib_journal = entry.get("journal") or entry.get("booktitle") or ""
    bib_date_str = entry.get("date", "")
    bib_abstract = entry.get("abstract", "")
    bib_url = entry.get("url", "") or entry.get("url_pdf", "")

    # Derive year/month/day from BibTeX date
    year_val, month_val, day_val = parse_bib_date(bib_date_str)

    # We'll use the same venue string for 'publication'
    bib_publication = bib_journal

    # Parse authors from BibTeX "author" field
    bib_authors_raw = entry.get("author", "")
    author_names = []
    if bib_authors_raw:
        # Typical BibTeX: "Last, First and Last2, First2"
        parts = [p.strip() for p in bib_authors_raw.replace("\n", " ").split(" and ") if p.strip()]
        author_names = parts

    # --- Build new lines for fields we manage ---
    new_field_lines = []

    # publication (venue for the theme)
    if bib_publication:
        new_field_lines.append(f'publication = "{toml_escape(bib_publication)}"\n')
    else:
        new_field_lines.append('publication = ""\n')

    # journal
    if bib_journal:
        new_field_lines.append(f'journal = "{toml_escape(bib_journal)}"\n')
    else:
        new_field_lines.append('journal = ""\n')

    # year
    if year_val:
        new_field_lines.append(f'year = "{toml_escape(year_val)}"\n')
    else:
        new_field_lines.append('year = ""\n')

    # date
    if year_val:
        date_value = f"{year_val}-{month_val or '01'}-{day_val or '01'}"
        new_field_lines.append(f'date = "{date_value}"\n')

    # abstract
    if bib_abstract:
        new_field_lines.append(f'abstract = "{toml_escape(bib_abstract)}"\n')
    else:
        new_field_lines.append('abstract = ""\n')

    # URLs
    new_field_lines.append('url_dataset = ""\n')
    new_field_lines.append(f'url_pdf = "{toml_escape(bib_url)}"\n')
    new_field_lines.append('url_project = ""\n')
    new_field_lines.append('url_slides = ""\n')
    new_field_lines.append('url_video = ""\n')

    # authors as [[authors]] blocks
    for author in author_names:
        member_flag = "true" if is_lab_member(author) else "false"
        new_field_lines.append('[[authors]]\n')
        new_field_lines.append(f'  name = "{toml_escape(author)}"\n')
        new_field_lines.append(f'  is_member = {member_flag}\n')

    # --- Build new front matter ---
    new_front = []
    # Keep opening +++
    new_front.append(front_lines[0])

    # Remove existing fields we manage: publication, journal, year, date, abstract, url_*, authors
    managed_prefixes = (
        "publication ",
        "journal ",
        "year ",
        "date ",
        "abstract ",
        "url_dataset ",
        "url_pdf ",
        "url_project ",
        "url_slides ",
        "url_video ",
        "authors ",
        "[[authors]]",
        "name ",
        "is_member ",
    )

    for line in front_lines[1:-1]:
        stripped = line.lstrip()
        if any(stripped.startswith(p) for p in managed_prefixes):
            continue
        new_front.append(line)

    # Insert our new fields and authors
    new_front.extend(new_field_lines)

    # Closing +++
    new_front.append(front_lines[-1])

    # Write back
    new_text = "".join(new_front + body_lines)
    file_path.write_text(new_text, encoding="utf-8")
    print(f"Filled metadata from BibTeX for {file_path}")
