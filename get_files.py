#!/usr/bin/env python3
import os
import json
from pathlib import Path

def get_files_info(directory):
    """Get all PDF and DOCX files with their sizes"""
    files = []
    try:
        for file in sorted(os.listdir(directory)):
            if file.endswith(('.pdf', '.docx')):
                filepath = os.path.join(directory, file)
                size_bytes = os.path.getsize(filepath)
                size_mb = size_bytes / (1024 * 1024)
                files.append({
                    "name": file,
                    "size": round(size_mb, 1),
                    "folder": os.path.basename(directory)
                })
    except Exception as e:
        print(f"Error: {e}")
    return files

# Get files from both folders
ebooks = get_files_info("/workspaces/ebooks/EBOOKS")
pengetahuan = get_files_info("/workspaces/ebooks/pengetahuan")

all_files = ebooks + pengetahuan

# Generate JavaScript code
js_code = "const books = [\n"
for file in all_files:
    js_code += f'    {{ name: "{file["name"]}", size: {file["size"]}, folder: "{file["folder"]}" }},\n'
js_code += "];"

print(js_code)
