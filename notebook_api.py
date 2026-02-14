#!/usr/bin/env python3
"""
AI Knowledge Base Chat Server - mirip NotebookLM
Fitur: Chat Q&A, document search, topic exploration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

# Knowledge Base dengan Q&A responses
KNOWLEDGE_BASE = {
    "hybrid": {
        "answer": "Sistem hybrid menggabungkan mesin pembakaran (bensin/diesel) dengan motor listrik. Motor listrik membantu pada kecepatan rendah untuk efisiensi maksimal. Sistem ini mengurangi konsumsi bahan bakar hingga 40% dan emisi CO2.",
        "sources": [
            "Electric and Hybrid Vehicles (3rd Edition) 2024",
            "HYBRID CONTROL SYSTEM.pdf",
            "Toyota Hybrid System Training Manual.pdf",
            "Understanding the Toyota Hybrid Braking System.pdf"
        ],
        "related": ["electric", "battery", "engine", "efficiency"]
    },
    "electric": {
        "answer": "Kendaraan listrik (EV) menggunakan baterai berkapasitas besar untuk menyimpan energi dan motor listrik AC/DC untuk propulsi. Keuntungan: emisi nol, biaya operasional rendah, performa tinggi. Kerugian: jarak terbatas, waktu charging, harga awal tinggi.",
        "sources": [
            "Electric and Hybrid Electric Vehicles (1st Edition) 2022",
            "Electric and Hybrid Vehicles (3rd Edition) 2024",
            "Emergency Response Guide 2025-NISSAN-LEAF.pdf",
            "Advanced battery management technologies for electric vehicles 2019.pdf"
        ],
        "related": ["hybrid", "battery", "charging", "motor"]
    },
    "adas": {
        "answer": "ADAS (Advanced Driver Assistance Systems) adalah teknologi keselamatan yang menggunakan sensor (kamera, radar, lidar) untuk memantau lingkungan. Fitur: adaptive cruise control, lane keeping, emergency braking, parking assist. Membutuhkan kalibrasi berkala untuk akurasi maksimal.",
        "sources": [
            "ADAS_Calibration.pdf",
            "ADAS MA600 Calibration Toolset User Manual.pdf",
            "TOYOTA SAFETY SENSE.pdf",
            "Advanced Driver Assistance Systems (ADAS) Specialist Test.pdf"
        ],
        "related": ["sensor", "safety", "camera", "calibration"]
    },
    "ecu": {
        "answer": "ECU (Engine Control Unit) adalah komputer kendaraan yang mengelola fungsi mesin real-time. Tugas: mengontrol injeksi bahan bakar, timing pengapian, udara masuk, emisi. Data dari berbagai sensor diproses untuk optimasi performa dan efisiensi.",
        "sources": [
            "Bosch Diesel Engine Management Systems and Components.pdf",
            "Engine-Management-Systems-Product-Information-Catalogue.pdf",
            "Service Manual Toyota 2NR-FE.pdf"
        ],
        "related": ["engine", "sensor", "fuel", "control"]
    },
    "battery": {
        "answer": "Baterai kendaraan listrik menyimpan energi kimia dan mengubahnya menjadi listrik. Teknologi terbaru: LiFePO4 (aman, daya tahan lama), NCA, NCM. Spesifikasi penting: kapasitas (kWh), tegangan, siklus hidup. Pengelolaan termal krusial untuk performa optimal.",
        "sources": [
            "Advanced battery management technologies for electric vehicles 2019.pdf",
            "SmartChargingSystem_Guide.pdf",
            "Monitor Cerdas untuk Baterai Otomotif.docx"
        ],
        "related": ["electric", "charging", "thermal", "management"]
    },
    "engine": {
        "answer": "Mesin mengonversi energi kimia bahan bakar menjadi tenaga mekanik. Dua tipe: spark ignition (bensin) dan compression ignition (diesel). Komponen utama: silinder, piston, crankshaft, valve. Parameter: displacement, compression ratio, power output.",
        "sources": [
            "Bosch Diesel Engine Management Systems and Components.pdf",
            "Engine Misfire and Fuel Trim Analysis Techniques.pdf",
            "Mitsubishi Engine 4m40 Repair Manual.pdf"
        ],
        "related": ["fuel", "ignition", "ecu", "performance"]
    },
    "sensor": {
        "answer": "Sensor mengukur kondisi fisik dan lingkungan kendaraan, mengirim sinyal ke ECU. Jenis utama: O2 (oksigen), MAF (mass airflow), throttle position, knock sensor, temperature sensors. Kalibrasi dan pembersihan preventif penting untuk akurasi.",
        "sources": [
            "Automotive Sensors Bosch.pdf",
            "Automobile Electrical and Electronic Systems 5th Edition.pdf"
        ],
        "related": ["ecu", "signal", "calibration", "diagnostic"]
    },
    "charging": {
        "answer": "Pengisian daya EV: Level 1 (120V, lambat), Level 2 (240V, menengah), DC Fast Charging (480V+, cepat). Smart charging mengoptimalkan waktu, biaya, kesehatan baterai. Charging protocol: CCS, Tesla SuperCharger, CHAdeMO. Waktu full-charge: 30 min - 8 jam tergantif level.",
        "sources": [
            "SmartChargingSystem_Guide.pdf",
            "Emergency Response Guide 2025-NISSAN-LEAF.pdf"
        ],
        "related": ["battery", "electric", "infrastructure", "grid"]
    },
    "transmission": {
        "answer": "Transmisi mentransmisikan tenaga dari engine/motor ke roda. Tipe: manual (shifting manual), automatic (shifting otomatis), CVT (continuous), dual-clutch. EV biasanya single-speed. Transmisi modern: efisien, respons cepat, smooth operation.",
        "sources": [
            "automatic transmission Aw03-72LE.pdf",
            "automatic transmission A-240L-A241E-A243.pdf",
            "LIST Automatic Transmission.pdf"
        ],
        "related": ["engine", "performance", "efficiency", "control"]
    },
    "wiring": {
        "answer": "Wiring diagram menunjukkan koneksi elektrik kendaraan. Simbol standar ISO menunjukkan komponen dan jalur arus. Warna kabel: merah (power), hitam (ground), kuning/hijau (signal). Diagram esensial untuk pemeliharaan, perbaikan, dan troubleshooting.",
        "sources": [
            "Manual All Toyota Wiring Diagram and Ecu Pinout.pdf",
            "CARA MEMBACA WIRRING DIAGRAM STANDARD ISO.pdf",
            "Toyota 3S-FE 3S-GE Electrical Wiring Diagrams.pdf"
        ],
        "related": ["electrical", "diagnostic", "circuit", "component"]
    }
}

# Daftar topik untuk exploration
TOPICS = {
    "Hybrid Systems": {
        "description": "Teknologi hybrid dan sistem kontrol kendaraan hybrid",
        "subtopics": ["Hybrid Architecture", "Control Systems", "Braking Systems", "Power Distribution"],
        "keywords": ["hybrid", "electric", "control", "efficiency"]
    },
    "Electric Vehicles": {
        "description": "Kendaraan listrik, baterai, dan charging infrastructure",
        "subtopics": ["EV Architecture", "Battery Management", "Charging Systems", "Motor Technology"],
        "keywords": ["electric", "battery", "charging", "motor", "ev"]
    },
    "Engine Management": {
        "description": "ECU, fuel injection, ignition, dan kontrol mesin",
        "subtopics": ["ECU Functions", "Fuel Injection", "Ignition Systems", "Emission Control"],
        "keywords": ["ecu", "engine", "fuel", "ignition", "management"]
    },
    "Safety & ADAS": {
        "description": "Sistem keselamatan dan ADAS (Advanced Driver Assistance)",
        "subtopics": ["ADAS Technologies", "Sensor Calibration", "Emergency Response", "Safety Features"],
        "keywords": ["adas", "safety", "sensor", "calibration", "emergency"]
    },
    "Electrical Systems": {
        "description": "Sistem kelistrikan, wiring, dan komponen elektronik",
        "subtopics": ["Wiring Diagrams", "Electrical Components", "Circuits", "Diagnostics"],
        "keywords": ["electrical", "wiring", "circuit", "component", "diagnostic"]
    }
}

# Saran pertanyaan untuk user
SUGGESTED_QUESTIONS = [
    "Apa itu sistem hybrid dan bagaimana cara kerjanya?",
    "Perbedaan antara kendaraan listrik dan hybrid?",
    "Bagaimana cara kerja ADAS dan sensor yang digunakan?",
    "Apa fungsi ECU dalam mengontrol mesin?",
    "Teknologi baterai apa yang paling baik untuk EV?",
    "Bagaimana sistem pengereman hybrid bekerja?",
    "Apa itu smart charging dan bagaimana cara kerjanya?",
    "Bagaimana cara membaca wiring diagram?",
    "Proses kalibrasi ADAS mengapa penting?",
    "Apa perbedaan transmisi manual dan automatic?"
]

def find_matching_knowledge(query):
    """Cari knowledge base yang paling relevan"""
    query_lower = query.lower()
    matches = []
    
    for keyword, info in KNOWLEDGE_BASE.items():
        if keyword in query_lower:
            matches.append((keyword, info, 100))
        else:
            # Check sources dan subtopics
            for source in info.get("sources", []):
                if any(q in source.lower() for q in query_lower.split()):
                    matches.append((keyword, info, 50))
                    break
            
            # Check related topics
            for related in info.get("related", []):
                if related in query_lower:
                    matches.append((keyword, info, 30))
                    break
    
    # Sort by relevance score
    matches.sort(key=lambda x: x[2], reverse=True)
    return matches[0] if matches else None

# ===== API ENDPOINTS =====

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat Q&A endpoint - mirip NotebookLM"""
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({
            "success": False,
            "error": "Parameter 'message' diperlukan"
        }), 400
    
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({
            "success": False,
            "error": "Pesan tidak boleh kosong"
        }), 400
    
    # Find matching knowledge
    match = find_matching_knowledge(user_message)
    
    if match:
        keyword, kb_info, relevance_score = match
        response = {
            "success": True,
            "message": user_message,
            "response": kb_info["answer"],
            "confidence": "high",
            "sources": kb_info["sources"],
            "related_topics": kb_info["related"],
            "topic": keyword,
            "timestamp": datetime.now().isoformat()
        }
    else:
        response = {
            "success": True,
            "message": user_message,
            "response": "Saya tidak memiliki informasi spesifik tentang topik ini dalam knowledge base. Silakan ajukan pertanyaan lain atau eksplorasi topik yang tersedia.",
            "confidence": "low",
            "sources": [],
            "related_topics": [],
            "timestamp": datetime.now().isoformat()
        }
    
    return jsonify(response)

@app.route('/api/topics', methods=['GET'])
def get_topics_list():
    """Dapatkan daftar topik untuk exploration"""
    return jsonify({
        "success": True,
        "topics": TOPICS,
        "topic_count": len(TOPICS)
    })

@app.route('/api/topic/<topic_name>', methods=['GET'])
def get_topic_details(topic_name):
    """Dapatkan detail topik tertentu"""
    if topic_name not in TOPICS:
        return jsonify({
            "success": False,
            "error": f"Topik '{topic_name}' tidak ditemukan"
        }), 404
    
    topic_info = TOPICS[topic_name]
    
    # Find related knowledge base entries
    related_kb = []
    for keyword in topic_info.get("keywords", []):
        if keyword in KNOWLEDGE_BASE:
            related_kb.append({
                "keyword": keyword,
                "answer": KNOWLEDGE_BASE[keyword]["answer"],
                "sources": KNOWLEDGE_BASE[keyword]["sources"]
            })
    
    return jsonify({
        "success": True,
        "topic": topic_name,
        "info": topic_info,
        "related_knowledge": related_kb
    })

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """Dapatkan saran pertanyaan"""
    return jsonify({
        "success": True,
        "suggestions": SUGGESTED_QUESTIONS,
        "total": len(SUGGESTED_QUESTIONS)
    })

@app.route('/api/knowledge-base', methods=['GET'])
def get_kb_stats():
    """Dapatkan statistik knowledge base"""
    kb_topics = list(KNOWLEDGE_BASE.keys())
    
    stats = {
        "total_topics": len(KNOWLEDGE_BASE),
        "total_questions_answered": sum(1 for _ in KNOWLEDGE_BASE),
        "total_sources": len([s for kb in KNOWLEDGE_BASE.values() for s in kb["sources"]]),
        "coverage_areas": list(TOPICS.keys()),
        "keywords": kb_topics
    }
    
    return jsonify({
        "success": True,
        "stats": stats,
        "knowledge_base": {
            k: {
                "answer_preview": v["answer"][:100] + "...",
                "sources_count": len(v["sources"]),
                "related_count": len(v["related"])
            }
            for k, v in KNOWLEDGE_BASE.items()
        }
    })

@app.route('/api/search', methods=['GET'])
def search_kb():
    """Search knowledge base"""
    query = request.args.get('q', '').lower()
    
    if not query or len(query) < 2:
        return jsonify({
            "success": False,
            "error": "Search query minimal 2 karakter"
        }), 400
    
    results = []
    
    # Search dalam knowledge base
    for keyword, info in KNOWLEDGE_BASE.items():
        score = 0
        
        if keyword in query:
            score += 100
        else:
            # Check answer
            if query in info["answer"].lower():
                score += 50
            
            # Check sources
            for source in info["sources"]:
                if query in source.lower():
                    score += 30
                    break
            
            # Check related
            for related in info["related"]:
                if related in query:
                    score += 20
        
        if score > 0:
            results.append({
                "topic": keyword,
                "answer": info["answer"][:100] + "...",
                "sources": info["sources"],
                "score": score
            })
    
    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return jsonify({
        "success": True,
        "query": query,
        "results": results[:5],
        "total": len(results)
    })

@app.route('/api', methods=['GET'])
def api_info():
    """API Info"""
    return jsonify({
        "name": "AI Knowledge Base Chat API",
        "version": "1.0",
        "type": "NotebookLM-like",
        "description": "Knowledge base AI untuk Q&A otomotif berdasarkan koleksi PDF",
        "endpoints": {
            "POST /api/chat": "Chat Q&A dengan AI",
            "GET /api/topics": "List semua topik",
            "GET /api/topic/<name>": "Detail topik tertentu",
            "GET /api/suggestions": "Saran pertanyaan",
            "GET /api/knowledge-base": "Stats knowledge base",
            "GET /api/search?q=keyword": "Search knowledge base"
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint tidak ditemukan",
        "help": "Kunjungi /api untuk dokumentasi"
    }), 404

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🤖 AI Knowledge Base Chat Server (NotebookLM-like)")
    print("=" * 70)
    print("\n📍 Server: http://localhost:5001")
    print("\n📡 API Endpoints:")
    print("   POST /api/chat - Chat Q&A dengan AI")
    print("   GET  /api/topics - Daftar topik")
    print("   GET  /api/suggestions - Saran pertanyaan")
    print("   GET  /api/knowledge-base - Statistik database")
    print("   GET  /api/search?q=keyword - Cari knowledge base")
    print("\n💡 Knowledge Base Covers:")
    print("   - Hybrid Systems, Electric Vehicles, ADAS")
    print("   -  Engine Management, Battery Technology")
    print("   - Electrical Systems, Sensor Calibration")
    print("\n✅ CORS Enabled - Dapat diakses dari web lain")
    print("\n🛑 Tekan Ctrl+C untuk menghentikan\n")
    print("=" * 70 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=False)
