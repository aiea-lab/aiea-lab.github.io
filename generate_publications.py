from pathlib import Path
import bibtexparser

bib_file = Path("publications.bib")
output_dir = Path("content/publication")
output_dir.mkdir(exist_ok=True)

with open(bib_file, "r") as f:
    bib_database = bibtexparser.load(f)

seen_files = {}

for entry in bib_database.entries:
    title_clean = entry['title'].lower().replace(" ", "-").replace(",", "").replace(":", "")
    year = entry.get('year', "unknown")
    base_filename = f"{title_clean}-{year}.md"

    # Make filename unique
    count = seen_files.get(base_filename, 0)
    if count > 0:
        filename = f"{title_clean}-{year}-{count+1}.md"
    else:
        filename = base_filename
    seen_files[base_filename] = count + 1

    file_path = output_dir / filename
    authors = entry.get('author', '')
    journal = entry.get('journal', entry.get('booktitle', ''))
    md_content = f"""+++
title = "{entry['title']}"
authors = "{authors}"
journal = "{journal}"
year = "{year}"
+++
"""
    with open(file_path, "w") as f:
        f.write(md_content)
    print(f"Created {file_path}")
