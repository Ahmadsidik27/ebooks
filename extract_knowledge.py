#!/usr/bin/env python3
"""
Script untuk mengekstrak teks dari semua PDF dan membuat knowledge base
"""

import os
import json
from pathlib import Path
import re

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

# Folder yang berisi PDF
EBOOKS_FOLDER = "/workspaces/ebooks/EBOOKS"
PENGETAHUAN_FOLDER = "/workspaces/ebooks/pengetahuan"
OUTPUT_FOLDER = "/workspaces/ebooks/knowledge_base"

# Buat folder output jika belum ada
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Ekstrak teks dari PDF menggunakan pdfplumber"""
    if not PDFPLUMBER_AVAILABLE:
        return None
    
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            # Ambil maksimal 5 halaman pertama untuk preview
            for i, page in enumerate(pdf.pages[:5]):
                text += f"\n--- Halaman {i+1} ---\n"
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error ekstrak {pdf_path}: {e}")
        return None

def create_knowledge_index():
    """Buat index pengetahuan dari semua PDF"""
    
    knowledge_base = {
        "metadata": {
            "total_documents": 0,
            "last_updated": str(Path.cwd()),
            "folders": ["EBOOKS", "pengetahuan"]
        },
        "documents": []
    }
    
    folders = [EBOOKS_FOLDER, PENGETAHUAN_FOLDER]
    
    for folder in folders:
        if not os.path.exists(folder):
            continue
        
        folder_name = os.path.basename(folder)
        print(f"Processing {folder_name}...")
        
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(('.pdf', '.docx')):
                filepath = os.path.join(folder, filename)
                file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
                
                # Ekstrak konten
                content = ""
                if filename.endswith('.pdf') and PDFPLUMBER_AVAILABLE:
                    content = extract_text_from_pdf(filepath)
                    if content:
                        content = content[:2000]  # Batasi 2000 karakter untuk preview
                
                doc_entry = {
                    "id": len(knowledge_base["documents"]),
                    "title": filename,
                    "folder": folder_name,
                    "size_mb": round(file_size, 2),
                    "type": "pdf" if filename.endswith('.pdf') else "docx",
                    "preview": content or "Konten tidak dapat diextrak",
                    "keywords": extract_keywords(filename)
                }
                
                knowledge_base["documents"].append(doc_entry)
                print(f"  ✓ {filename}")
    
    knowledge_base["metadata"]["total_documents"] = len(knowledge_base["documents"])
    
    # Simpan ke file
    kb_path = os.path.join(OUTPUT_FOLDER, "knowledge_base.json")
    with open(kb_path, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Knowledge base created: {kb_path}")
    print(f"   Total documents: {len(knowledge_base['documents'])}")
    
    return knowledge_base

def extract_keywords(filename):
    """Ekstrak keywords dari nama file"""
    keywords = []
    terms = [
        "Hybrid", "Electric", "EV", "ADAS", "ECU", "Engine", "Diesel", "Petrol",
        "Bosch", "Toyota", "Honda", "Suzuki", "Mitsubishi", "Daihatsu", "Hyundai",
        "CAN", "OBD", "Wiring", "Service", "Manual", "Training", "Repair",
        "Management", "Control", "System", "Sensor", "Ignition", "Fuel"
    ]
    
    for term in terms:
        if term.lower() in filename.lower():
            keywords.append(term)
    
    return keywords[:5]

def create_simple_vectordb():
    """Buat simple vector database untuk search"""
    kb_path = os.path.join(OUTPUT_FOLDER, "knowledge_base.json")
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    # Buat search index
    search_index = {
        "by_keyword": {},
        "by_folder": {},
        "by_type": {}
    }
    
    for doc in kb["documents"]:
        # Index by keywords
        for keyword in doc["keywords"]:
            if keyword not in search_index["by_keyword"]:
                search_index["by_keyword"][keyword] = []
            search_index["by_keyword"][keyword].append(doc["id"])
        
        # Index by folder
        folder = doc["folder"]
        if folder not in search_index["by_folder"]:
            search_index["by_folder"][folder] = []
        search_index["by_folder"][folder].append(doc["id"])
        
        # Index by type
        doc_type = doc["type"]
        if doc_type not in search_index["by_type"]:
            search_index["by_type"][doc_type] = []
        search_index["by_type"][doc_type].append(doc["id"])
    
    # Simpan search index
    index_path = os.path.join(OUTPUT_FOLDER, "search_index.json")
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, indent=2)
    
    print(f"✅ Search index created: {index_path}")
    
    # Tampilkan statistik
    print("\n📊 Search Index Statistics:")
    print(f"   Keywords: {len(search_index['by_keyword'])}")
    print(f"   Folders: {len(search_index['by_folder'])}")
    print(f"   Types: {len(search_index['by_type'])}")

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 Mengekstrak Knowledge Base dari PDF...")
    print("=" * 60 + "\n")
    
    # Cek apakah pdfplumber tersedia
    if not PDFPLUMBER_AVAILABLE:
        print("⚠️  pdfplumber tidak terinstall")
        print("   Install dengan: pip install pdfplumber")
        print("\nMembuat knowledge base tanpa ekstraksi teks PDF...\n")
    
    # Create knowledge base
    kb = create_knowledge_index()
    
    # Create search index
    create_simple_vectordb()
    
    print("\n" + "=" * 60)
    print("✅ Knowledge base creation complete!")
    print("=" * 60)
