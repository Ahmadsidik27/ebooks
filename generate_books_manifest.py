#!/usr/bin/env python3
"""
Generate manifest file containing all books from EBOOKS and pengetahuan folders
"""
import os
import json
from pathlib import Path
from datetime import datetime

EBOOKS_FOLDER = Path("EBOOKS")
PENGETAHUAN_FOLDER = Path("pengetahuan")

books = []

# Get EBOOKS
for pdf_file in sorted(EBOOKS_FOLDER.glob("*.pdf")):
    size_mb = pdf_file.stat().st_size / (1024 * 1024)
    books.append({
        "id": len(books) + 1,
        "title": pdf_file.stem,
        "filename": pdf_file.name,
        "size_mb": round(size_mb, 2),
        "source": "EBOOKS",
        "path": f"EBOOKS/{pdf_file.name}"
    })

# Get Pengetahuan
for pdf_file in sorted(PENGETAHUAN_FOLDER.glob("*.pdf")):
    size_mb = pdf_file.stat().st_size / (1024 * 1024)
    books.append({
        "id": len(books) + 1,
        "title": pdf_file.stem,
        "filename": pdf_file.name,
        "size_mb": round(size_mb, 2),
        "source": "pengetahuan",
        "path": f"pengetahuan/{pdf_file.name}"
    })

manifest = {
    "total_books": len(books),
    "total_size_mb": round(sum(b["size_mb"] for b in books), 2),
    "ebooks_count": len([b for b in books if b["source"] == "EBOOKS"]),
    "pengetahuan_count": len([b for b in books if b["source"] == "pengetahuan"]),
    "generated": datetime.now().isoformat(),
    "books": books
}

# Save as JSON
with open("books_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

# Save as JavaScript
with open("books_data.js", "w") as f:
    f.write(f"const booksData = {json.dumps(manifest, indent=2)};")

print(f"✅ Generated manifest with {len(books)} books")
print(f"Total size: {manifest['total_size_mb']} MB")
