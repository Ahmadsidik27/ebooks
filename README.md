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

## 📂 Struktur Direktori

```
ebooks/
├── README.md                   # Dokumentasi project
├── server.py                   # Static file HTTP server (port 8000)
├── api.py                      # REST API server (port 5000)
├── notebook_api.py             # AI Knowledge Base API (port 5001)
├── extract_knowledge.py        # PDF knowledge extraction tool
├── get_files.py               # File listing utility
│
├── EBOOKS/                     # 41 e-book files (573 MB)
├── pengetahuan/               # 88 e-book files (362 MB)
├── knowledge_base/            # Generated knowledge base data
│
├── home.html                  # Landing page
├── index.html                 # Library catalog
└── chat.html                  # AI chat interface
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

### GitHub Pages (Frontend Only)
- Push HTML/CSS/JS ke gh-pages
- API URLs ke external endpoints

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
