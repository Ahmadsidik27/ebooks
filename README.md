# E-Books Management & AI Knowledge Base

Platform terintegrasi untuk manajemen koleksi e-book dengan AI chatbot berbasis knowledge base, mirip dengan Google NotebookLM.

![Status](https://img.shields.io/badge/status-active-brightgreen) ![Python](https://img.shields.io/badge/python-3.8+-blue) ![License](https://img.shields.io/badge/license-MIT-green)

## 📚 Features

### 1. **E-Books Library**
- Katalog 129 e-book dengan fitur pencarian real-time
- Filter berdasarkan ukuran file (< 5MB, 5-20MB, > 20MB)
- Grid dan list view untuk fleksibilitas tampilan
- Statistik koleksi (total buku, ukuran total, rata-rata ukuran)
- Source terpisah: EBOOKS (41 file) dan pengetahuan (88 file)

### 2. **REST API**
- 7 endpoint API untuk akses data external
- CORS enabled untuk cross-origin requests
- Dokumentasi endpoint lengkap
- JSON response format

### 3. **AI Knowledge Base Chat**
- Chatbot dengan 10 topic inti:
  - Hybrid Systems, Electric Vehicles, Engine Management
  - Safety & ADAS, Electrical Systems
- Pencarian knowledge base dengan keyword matching
- Saran pertanyaan otomatis
- Source tracking untuk setiap jawaban
- Confidence level indicator

### 4. **Web Interfaces**
- **home.html**: Landing page dengan presentasi profesional
- **index.html**: Katalog e-book dengan search & filter
- **chat.html**: AI chat interface dengan sidebar navigation

### 5. **PDF to HTML Converter**
- Konversi otomatis PDF ke format HTML yang dapat dibaca di browser
- Preserve formatting, images, dan struktur dokumen
- Generate index HTML untuk navigasi semua files
- Responsive design dengan styling modern
- Support untuk page navigation, text extraction, dan tables
- Cepat dan aman untuk koleksi besar (41 PDF files)

### 6. **Static Website untuk GitHub Pages** ✨ NEW
- Deploy 124+ e-book ke GitHub Pages dalam hitungan menit
- Search & filter functionality tanpa backend
- Direct PDF download links
- Responsive design (mobile/tablet/desktop)
- 100% static HTML/CSS/JS - cepat & aman
- Statistics dashboard (total books, size, breakdown)
- Automated deployment script tersedia

## 📂 Struktur Direktori

```
ebooks/
├── README.md                        # Dokumentasi project
├── requirements.txt                 # Python dependencies
├── GITHUB_PAGES_DEPLOY.md           # GitHub Pages deployment guide ✨ NEW
│
├── server.py                        # Static file HTTP server (port 8000)
├── api.py                           # REST API server (port 5000)
├── notebook_api.py                  # AI Knowledge Base API (port 5001)
├── extract_knowledge.py             # PDF knowledge extraction tool
├── pdf_to_html_converter.py         # PDF to HTML converter tool
├── generate_books_manifest.py       # Generate book manifest JSON ✨ NEW
├── get_files.py                     # File listing utility
│
├── Static Website Files ✨ NEW:
├── index-github-pages.html          # Main static website  
├── books_data.js                    # Book catalog (generated)
├── books_manifest.json              # Book metadata (generated)
├── web-server-static.py             # Local web server for testing
├── deploy-to-github-pages.sh        # Auto-deploy script
├── static-website-setup.html        # Interactive setup guide
│
├── EBOOKS/                          # 41 e-book files (573 MB) - Original PDF
├── HTML_EBOOKS/                     # Converted HTML files
│   ├── index.html                   # Index semua HTML books
│   ├── *.html                       # Individual book pages
│   └── images/                      # Page screenshots
├── pengetahuan/                     # 88 e-book files (362 MB)
├── knowledge_base/                  # Generated knowledge base data
│
├── home.html                        # Landing page (Flask app)
├── index.html                       # Library catalog (Flask app)
└── chat.html                        # AI chat interface (Flask app)
```

## 🚀 Quick Start

### Prerequisites
```bash
python3 --version  # 3.8+
pip install flask flask-cors
```

### Running the Application

Jalankan 3 server di terminal berbeda:

#### Terminal 1: Static File Server (Port 8000)
```bash
python3 server.py
# Akses: http://localhost:8000
```

#### Terminal 2: REST API Server (Port 5000)
```bash
python3 api.py
# API Docs: http://localhost:5000/api
```

#### Terminal 3: AI Knowledge Base (Port 5001)
```bash
python3 notebook_api.py
# Knowledge Base: http://localhost:5001/api
```

### Akses Interface
- **Home Page**: http://localhost:8000/home.html
- **Library**: http://localhost:8000/index.html
- **AI Chat**: http://localhost:8000/chat.html
- **HTML Books**: http://localhost:8000/HTML_EBOOKS/index.html ✨ NEW

## 🔄 PDF to HTML Converter (NEW Feature!)

Untuk mengkonversi semua PDF di folder EBOOKS menjadi HTML yang dapat dibaca di browser:

### Instalasi Dependencies
```bash
pip install -r requirements.txt
# atau manual:
pip install pdfplumber pdf2image Pillow weasyprint reportlab PyPDF2
```

### Cara Penggunaan

**Konversi semua PDF ke HTML:**
```bash
python3 pdf_to_html_converter.py
```

Apa yang akan terjadi:
1. ✅ Scan folder EBOOKS untuk semua file PDF
2. ✅ Extract teks dan metadata dari setiap PDF
3. ✅ Konversi page PDF ke images (PNG) untuk preview
4. ✅ Generate HTML files dengan styling modern dan responsive
5. ✅ Buat index.html untuk navigasi semua buku
6. ✅ Simpan semua files di folder `HTML_EBOOKS/`

### Hasil
- **41 HTML files** (satu untuk setiap PDF di EBOOKS/)
- **index.html** - Navigation page untuk semua buku
- **images/** - Folder berisi preview images dari PDF pages
- **Responsive design** - Readable di desktop, tablet, mobile

Buka browser dan akses:
- `http://localhost:8000/HTML_EBOOKS/` - View semua buku dalam HTML
- Atau langsung buka `HTML_EBOOKS/index.html` di file manager

## 🌐 Static Website untuk GitHub Pages (NEW!)

Hosting website statis ke GitHub Pages dengan semua 124+ buku (EBOOKS + pengetahuan).

### Setup Cepat (5 Menit)

```bash
# 1. Generate manifest
python3 generate_books_manifest.py

# 2. Test locally
python3 web-server-static.py
# Buka: http://localhost:8000/index-github-pages.html

# 3. Deploy ke GitHub
chmod +x deploy-to-github-pages.sh
./deploy-to-github-pages.sh YOUR_USERNAME

# Website tersedia di: https://YOUR_USERNAME.github.io/ebooks/
```

### Fitur Website Statis

✨ **Features:**
- 📚 Katalog lengkap 124+ buku (EBOOKS + pengetahuan)
- 🔍 Search & filter functionality
- 📊 Statistics dashboard
- 🎨 Responsive design (mobile/tablet/desktop)
- ⬇️ Direct PDF download links
- 💻 100% static HTML/CSS/JS - tidak perlu backend
- ⚡ Cepat, aman, dan scalable
- 🚀 Auto-deploy script tersedia

### File-file Penting

| File | Fungsi |
|------|--------|
| `index-github-pages.html` | Main website file (rename ke `index.html`) |
| `books_data.js` | Book catalog data (auto-generated) |
| `books_manifest.json` | Book metadata (auto-generated) |
| `deploy-to-github-pages.sh` | Automated deployment script |
| `web-server-static.py` | Local testing server |
| `GITHUB_PAGES_DEPLOY.md` | Detailed deployment guide |
| `static-website-setup.html` | Interactive setup helper |

### Dokumentasi

Baca panduan lengkap di:
- **[GITHUB_PAGES_DEPLOY.md](GITHUB_PAGES_DEPLOY.md)** - Step-by-step deployment
- **[static-website-setup.html](static-website-setup.html)** - Interactive HTML guide

### Struktur Data Website

Website menggunakan data dari file `books_data.js`:
```javascript
{
  "total_books": 124,
  "total_size_mb": 932.63,
  "ebooks_count": 41,
  "pengetahuan_count": 83,
  "books": [...]  // Array of all books
}
```

Manifest auto-update saat menjalankan `generate_books_manifest.py`


## 📡 API Endpoints

### Books API (Port 5000)

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api` | Info & dokumentasi |
| GET | `/api/books` | Semua buku (pagination) |
| GET | `/api/books/search?q=keyword` | Search buku |
| GET | `/api/books/filter?size=large` | Filter by size |
| GET | `/api/stats` | Statistik koleksi |
| GET | `/api/categories` | Kategori |
| GET | `/api/folders` | List folder |

**Contoh:**
```bash
curl http://localhost:5000/api/books/search?q=hybrid
curl http://localhost:5000/api/books/filter?size=large
```

### AI Knowledge Base API (Port 5001)

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/chat` | Chat dengan AI |
| GET | `/api/topics` | List topics |
| GET | `/api/topic/<name>` | Detail topic |
| GET | `/api/suggestions` | Saran pertanyaan |
| GET | `/api/search?q=keyword` | Search KB |
| GET | `/api/knowledge-base` | Stats KB |

**Contoh:**
```bash
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Apa itu hybrid system?"}'
```

## 🔧 Technical Stack

| Komponen | Technology |
|---------|-----------|
| Backend | Python 3, Flask, Flask-CORS |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Architecture | 3 Independent Microservices |
| API Format | JSON with CORS |

## 📊 Statistics

- **Total Books**: 129
- **EBOOKS**: 41 files (573 MB)
- **Pengetahuan**: 88 files (362 MB)
- **Total Size**: 935 MB
- **Avg File Size**: 7.4 MB
- **KB Topics**: 10 core topics

## 🚢 Deployment

### Railway.app (Recommended)
```bash
pip freeze > requirements.txt
# Setup di railway.app
railway up
```

### Heroku
```bash
# Create Procfile
echo "web: python3 server.py" > Procfile
heroku create
git push heroku main
```

### GitHub Pages (Static Website) ✨ NEW - Recommended!
```bash
# Generate books manifest
python3 generate_books_manifest.py

# Test locally
python3 web-server-static.py
# Akses: http://localhost:8000/index-github-pages.html

# Deploy otomatis
chmod +x deploy-to-github-pages.sh
./deploy-to-github-pages.sh YOUR_USERNAME

# Website tersedia di:
# https://YOUR_USERNAME.github.io/ebooks/
```

**Features:**
- 124+ buku dari EBOOKS + pengetahuan (total 935 MB)
- Search & filter by size/name
- Responsive design (mobile/tablet/desktop)
- Direct PDF download links
- 100% static - cepat & aman
- No backend required

**Setup Guide:** Lihat [GITHUB_PAGES_DEPLOY.md](GITHUB_PAGES_DEPLOY.md)  
**Interactive Setup:** Buka [static-website-setup.html](static-website-setup.html)

### VPS (Full Control)
- Rent VPS (DigitalOcean, Linode)
- Install Python & Flask
- Setup systemd services

## 📝 Knowledge Base Topics

1. Hybrid Systems - Teknologi hybrid vehicle
2. Electric Vehicles - Kendaraan listrik
3. ADAS - Advanced Driver Assistance
4. ECU - Engine Control Unit
5. Battery - Battery management
6. Engine - Internal combustion
7. Sensor - Vehicle sensors
8. Charging - Charging infrastructure
9. Transmission - Transmission system
10. Wiring - Electrical wiring

## 🔍 Development

Cek semua server berjalan:
```bash
curl -I http://localhost:8000
curl -I http://localhost:5000/api
curl -I http://localhost:5001/api
```

## 📄 License

MIT License

## 👤 Author

Dibuat dengan ❤️ untuk knowledge management dan e-book organization

---

**Status**: Production Ready ✅
**Last Updated**: February 2026
