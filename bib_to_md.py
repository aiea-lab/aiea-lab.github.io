import bibtexparser
from pathlib import Path

# Path to your bibtex file
bib_file = Path("publications.bib")
output_dir = Path("content/publication")
output_dir.mkdir(exist_ok=True)

with open(bib_file, "r") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

for entry in bib_database.entries:
    # Generate a file name from title + year
    title_clean = entry['title'].lower().replace(" ", "-").replace(",", "").replace(":", "")
    year = entry.get('year', "unknown")
    filename = f"{title_clean}-{year}.md"

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
