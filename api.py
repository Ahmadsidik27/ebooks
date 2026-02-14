#!/usr/bin/env python3
"""
API Server untuk Perpustakaan E-Books Otomotif
Menyediakan REST API untuk akses data buku dari aplikasi lain
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS untuk semua routes

# Data buku (sama seperti di index.html)
BOOKS_DATA = [
    # EBOOKS Folder
    {"name": "ACDELCO - HYBRID & ELECTRIC VEHICLE.pdf", "size": 7.0, "folder": "EBOOKS"},
    {"name": "ADAS MA600 Calibration Toolset User Manual.pdf", "size": 1.4, "folder": "EBOOKS"},
    {"name": "ADAS_Calibration.pdf", "size": 3.5, "folder": "EBOOKS"},
    {"name": "AUTOMOTIVE CONTROL SYSTEMS.pdf", "size": 6.5, "folder": "EBOOKS"},
    {"name": "Advanced Driver Assistance Systems (ADAS) Specialist Test.pdf", "size": 1.4, "folder": "EBOOKS"},
    {"name": "Advanced battery management technologies for electric vehicles 2019.pdf", "size": 16, "folder": "EBOOKS"},
    {"name": "Automobile Electrical and Electronic Systems 5th Edition by Tom Denton.pdf", "size": 50, "folder": "EBOOKS"},
    {"name": "Automotive Air-conditioning and Climate Control Systems by Steven Daly.pdf", "size": 7.7, "folder": "EBOOKS"},
    {"name": "Automotive Sensors Bosch.pdf", "size": 3.7, "folder": "EBOOKS"},
    {"name": "Automotive-ECU-architecture-and-logic.pdf", "size": 7.6, "folder": "EBOOKS"},
    {"name": "Bosch Automotive Electrics and Automotive Electronics.pdf", "size": 7.8, "folder": "EBOOKS"},
    {"name": "Bosch Automotive Networking, Driving Stability Systems, Electronics.pdf", "size": 12, "folder": "EBOOKS"},
    {"name": "Bosch Diesel Engine Management Systems and Components.pdf", "size": 13, "folder": "EBOOKS"},
    {"name": "Bosch Electronic Diesel Control (EDC) Edition 2001.pdf", "size": 1.8, "folder": "EBOOKS"},
    {"name": "CANopenTechnical Manual.pdf", "size": 8.2, "folder": "EBOOKS"},
    {"name": "DENSO Engine-Management-System-Catalogue.pdf", "size": 3.2, "folder": "EBOOKS"},
    {"name": "Denso aircond catalogue-2020.pdf", "size": 20, "folder": "EBOOKS"},
    {"name": "Denso-RV-HVAC-Service-Manual.pdf", "size": 2.5, "folder": "EBOOKS"},
    {"name": "Diagnosing Keys & Immobilizer Systems.pdf", "size": 17, "folder": "EBOOKS"},
    {"name": "Ecu Modules Repair Ebook.pdf", "size": 12, "folder": "EBOOKS"},
    {"name": "Electric and Hybrid Electric Vehicles (1st Edition) 2022.pdf", "size": 69, "folder": "EBOOKS"},
    {"name": "Electric and Hybrid Vehicles (3rd Edition) 2024.pdf", "size": 95, "folder": "EBOOKS"},
    {"name": "Engine Misfire and Fuel Trim Analysis Techniques.pdf", "size": 34, "folder": "EBOOKS"},
    {"name": "Engine-Management-Systems-Product-Information-Catalogue.pdf", "size": 3.2, "folder": "EBOOKS"},
    {"name": "Gasoline_Engine_Management_Systems_and_Components.pdf", "size": 11, "folder": "EBOOKS"},
    {"name": "Hybrid and Electric Vehicles.pdf", "size": 5.3, "folder": "EBOOKS"},
    {"name": "ISUZU SERVICE TRAINING.pdf", "size": 9.7, "folder": "EBOOKS"},
    {"name": "Introduction to ADAS.pdf", "size": 1.9, "folder": "EBOOKS"},
    {"name": "Kia Automotive Electrical Diagnosis Course.pdf", "size": 17, "folder": "EBOOKS"},
    {"name": "MPX (multiplex communication) System .pdf", "size": 3.3, "folder": "EBOOKS"},
    {"name": "Materi CR-V Hybrid.pdf", "size": 9.8, "folder": "EBOOKS"},
    {"name": "Materi Training Electronic Fuel Injection-Engine Management.pdf", "size": 4.3, "folder": "EBOOKS"},
    {"name": "Mitsubishi Engine 4m40 Repair Manual.pdf", "size": 8.6, "folder": "EBOOKS"},
    {"name": "Modern Automotive Technology 7th.pdf", "size": 39, "folder": "EBOOKS"},
    {"name": "Modern Car Handbook 2020.pdf", "size": 6.5, "folder": "EBOOKS"},
    {"name": "Service Diagnosis and Measurement Manual SAIC Motor.pdf", "size": 19, "folder": "EBOOKS"},
    {"name": "TROUBLESHOOTING AUTOMOTIVE COMPUTER.pdf", "size": 2.1, "folder": "EBOOKS"},
    {"name": "Toyota Hybrid System (THS) 1 & 2 Operation.pdf", "size": 20, "folder": "EBOOKS"},
    {"name": "Toyota Hybrid System Training Manual.pdf", "size": 0.86, "folder": "EBOOKS"},
    {"name": "Troubleshooting Automotive Computer Systems.pdf", "size": 2.3, "folder": "EBOOKS"},
    {"name": "Understanding Automotive Electronics.pdf", "size": 17, "folder": "EBOOKS"},
    
    # Pengetahuan Folder
    {"name": "Emergency Response Quick Guide_2022 - 2024 Corolla HV.pdf", "size": 6.3, "folder": "pengetahuan"},
    {"name": "Emergency Response Quick Reference_2023-2024 Corolla Cross HV.pdf", "size": 5.5, "folder": "pengetahuan"},
    {"name": "Toyota Hilux HV T ERG 103 D.pdf", "size": 3.3, "folder": "pengetahuan"},
    {"name": "Daihatsu Installs the eSMART HYBRID.pdf", "size": 0.52, "folder": "pengetahuan"},
    {"name": "Emergency Response Guide 2025-NISSAN-LEAF.pdf", "size": 3.8, "folder": "pengetahuan"},
    {"name": "EPS HONDA FIT.pdf", "size": 8.6, "folder": "pengetahuan"},
    {"name": "Mild Hybrid System and Micro Hybrid System.pdf", "size": 0.64, "folder": "pengetahuan"},
    {"name": "For Dismantlers GRAND VITARA.pdf", "size": 3.4, "folder": "pengetahuan"},
    {"name": "SWIFT SPORT Dismantling Manual.pdf", "size": 0.84, "folder": "pengetahuan"},
    {"name": "Understanding the Toyota Hybrid Braking System.pdf", "size": 5.0, "folder": "pengetahuan"},
    {"name": "Toyota Corolla 1.6, 4A-FE, 4AFE, diagrama de la ECU, ECU pinout.pdf", "size": 4.3, "folder": "pengetahuan"},
    {"name": "How To find Toyota Ignition System Faults Fast.pdf", "size": 5.0, "folder": "pengetahuan"},
    {"name": "Ford 2020 - 2023 MY OBD System Operation.pdf", "size": 0.73, "folder": "pengetahuan"},
    {"name": "CAN-Training.pdf", "size": 0.30, "folder": "pengetahuan"},
    {"name": "FE series FE6,FE6T & FE6TA.pdf", "size": 0.92, "folder": "pengetahuan"},
    {"name": "automatic transmission Aw03-72LE.pdf", "size": 5.7, "folder": "pengetahuan"},
    {"name": "automatic transmission A-240L-A241E-A243.pdf", "size": 3.8, "folder": "pengetahuan"},
    {"name": "TOYOTA ENGINE IMMOBILISER SYSTEM.pdf", "size": 1.3, "folder": "pengetahuan"},
    {"name": "TROUBLESHOOTING SUZUKI CARRY FUTURA 1.5 G15A.pdf", "size": 2.5, "folder": "pengetahuan"},
    {"name": "Kontrol Injeksi Bahan Bakar dan Pemutus Bahan Bakar.pdf", "size": 0.50, "folder": "pengetahuan"},
    {"name": "Toyota Course; Idle air control system.pdf", "size": 1.1, "folder": "pengetahuan"},
    {"name": "SmartChargingSystem_Guide.pdf", "size": 3.5, "folder": "pengetahuan"},
    {"name": "ETACS Functionality Development for the OUTLANDER.pdf", "size": 1.4, "folder": "pengetahuan"},
    {"name": "Diesel Injection Pump HINO Dutro - TOYOTA Dyna (N04C-T).pdf", "size": 1.1, "folder": "pengetahuan"},
    {"name": "LIST Automatic Transmission.pdf", "size": 17, "folder": "pengetahuan"},
    {"name": "PANDUAN FITUR, TROUBLESHOOTING, WIRING & REGISTER REMOTE CONTROL Grand Livina SV.pdf", "size": 0.76, "folder": "pengetahuan"},
    {"name": "MULTIPLEX COMMUNICATION SYSTEM AYLA.pdf", "size": 0.78, "folder": "pengetahuan"},
    {"name": "Honda CVT Manual (AAMCO).pdf", "size": 6.8, "folder": "pengetahuan"},
    {"name": "Power Sliding Doors Honda Odyssey.pdf", "size": 2.3, "folder": "pengetahuan"},
    {"name": "Table of Applicable ECU.pdf", "size": 1.4, "folder": "pengetahuan"},
    {"name": "IDENTIFYING CALIBRATION CODES ON COMMON RAIL.pdf", "size": 0.19, "folder": "pengetahuan"},
    {"name": "DTCList_MD1 canter.pdf", "size": 1.2, "folder": "pengetahuan"},
    {"name": "Transponder and Remote Controls Programming Manually.pdf", "size": 2.2, "folder": "pengetahuan"},
    {"name": "Spark Plug & Diesel Glow Plug CATALOGUE 2017-18.pdf", "size": 5.5, "folder": "pengetahuan"},
    {"name": "Table DTC (Hex) Root Description Failure.pdf", "size": 1.0, "folder": "pengetahuan"},
    {"name": "HONDA DUAL MODE CHARGING SYSTEM.pdf", "size": 1.1, "folder": "pengetahuan"},
    {"name": "MATIC [A4Q-D1]terios.pdf", "size": 1.9, "folder": "pengetahuan"},
    {"name": "Toyota Smart Entry & Start System.pdf", "size": 2.6, "folder": "pengetahuan"},
    {"name": "VITARA  S-CROSS  Strong Hybrid System.pdf", "size": 1.5, "folder": "pengetahuan"},
    {"name": "SWIFT SPORT  SHVS Mild Hybrid System.pdf", "size": 0.84, "folder": "pengetahuan"},
    {"name": "OBD System Operation.pdf", "size": 0.73, "folder": "pengetahuan"},
    {"name": "Cars-LCV Ecu Type List.pdf", "size": 1.0, "folder": "pengetahuan"},
    {"name": "CARA MEMBACA WIRRING DIAGRAM STANDARD ISO.pdf", "size": 0.92, "folder": "pengetahuan"},
    {"name": "TOYOTA HYBRID CONTROL SYSTEM.pdf", "size": 0.17, "folder": "pengetahuan"},
    {"name": "HYBRID CONTROL SYSTEM.pdf", "size": 9.3, "folder": "pengetahuan"},
    {"name": "CAN_bus_diagnostics.pdf", "size": 0.45, "folder": "pengetahuan"},
    {"name": "Hyundai Emergency Response Guide - KONA Electric.pdf", "size": 3.2, "folder": "pengetahuan"},
    {"name": "KONA HybridEmergency Response Guide.pdf", "size": 3.9, "folder": "pengetahuan"},
    {"name": "IONIQ5-NE-EV-Emergency-Response-Guide_Aust_Final-2021.pdf", "size": 2.0, "folder": "pengetahuan"},
    {"name": "EMERGENCY RESPONSE GUIDE RENAULT GROUP.pdf", "size": 1.5, "folder": "pengetahuan"},
    {"name": "Emergency Response Guide 2025 CR-V eFCEV.pdf", "size": 3.3, "folder": "pengetahuan"},
    {"name": "Emergency Response Guide 2025 Civic Hybrid.pdf", "size": 1.3, "folder": "pengetahuan"},
    {"name": "Hyundai Ioniq HEVEmergency Response Guide .pdf", "size": 2.1, "folder": "pengetahuan"},
    {"name": "iQ EVElectric Vehicle.pdf", "size": 2.2, "folder": "pengetahuan"},
    {"name": "VolkswagenAudi Vehicle Communication Software Manual.pdf", "size": 0.89, "folder": "pengetahuan"},
    {"name": "Toyota 3S-FE 3S-GE Electrical Wiring Diagrams.pdf", "size": 9.3, "folder": "pengetahuan"},
    {"name": "Hybrid Vehicle Systems Panel Trainer_LJCreate.pdf", "size": 4.1, "folder": "pengetahuan"},
    {"name": "HONDA AIMING DRIVING SUPPORT SYSTEMS.pdf", "size": 0.75, "folder": "pengetahuan"},
    {"name": "Service Manual Toyota 2NR-FE.pdf", "size": 9.9, "folder": "pengetahuan"},
    {"name": "Manual All Toyota Wiring Diagram and Ecu Pinout.pdf", "size": 128, "folder": "pengetahuan"},
    {"name": "Connector Pinout North America, Europe and Asia OBD Pinouts.pdf", "size": 0.94, "folder": "pengetahuan"},
    {"name": "Ignition Coils all Brands.pdf", "size": 39, "folder": "pengetahuan"},
    {"name": "keys and Control Units  Immobilizer for all brands.pdf", "size": 2.7, "folder": "pengetahuan"},
    {"name": "identifikasi-efi-soluna_.pdf", "size": 1.9, "folder": "pengetahuan"},
    {"name": "Materi Training Honda eN1.pdf", "size": 3.2, "folder": "pengetahuan"},
    {"name": "Materi Training Honda Step WGN.pdf", "size": 4.1, "folder": "pengetahuan"},
    {"name": "Automotive Electronic.pdf", "size": 2.8, "folder": "pengetahuan"},
    {"name": "Version List Engine Ecu maker & model.pdf", "size": 4.5, "folder": "pengetahuan"},
    {"name": "CAN BUS & LIN BUS education board.pdf", "size": 1.6, "folder": "pengetahuan"},
    {"name": "Membaca & Memahami Data OBD II.pdf", "size": 0.23, "folder": "pengetahuan"}
]

# Helper functions
def get_size_category(size_mb):
    """Kategorisasi ukuran file"""
    if size_mb < 5:
        return "small"
    elif size_mb < 20:
        return "medium"
    else:
        return "large"

def calculate_stats():
    """Hitung statistik dari semua buku"""
    total_books = len(BOOKS_DATA)
    total_size = sum(book["size"] for book in BOOKS_DATA)
    avg_size = total_size / total_books if total_books > 0 else 0
    
    return {
        "total_books": total_books,
        "total_size_mb": round(total_size, 2),
        "average_size_mb": round(avg_size, 2),
        "folders": len(set(book["folder"] for book in BOOKS_DATA))
    }

# API Routes

@app.route('/api', methods=['GET'])
def api_info():
    """Informasi API"""
    return jsonify({
        "name": "Perpustakaan E-Books Otomotif API",
        "version": "1.0",
        "description": "REST API untuk akses data perpustakaan e-books otomotif",
        "endpoints": {
            "GET /api/books": "Dapatkan semua buku",
            "GET /api/books?page=1&limit=10": "Dapatkan buku dengan pagination",
            "GET /api/books/search?q=keyword": "Cari buku berdasarkan keyword",
            "GET /api/books/filter?size=large": "Filter buku berdasarkan ukuran (small/medium/large)",
            "GET /api/stats": "Dapatkan statistik perpustakaan",
            "GET /api/categories": "Dapatkan kategori buku",
            "GET /api/download-link?folder=EBOOKS&file=name": "Dapatkan link download"
        }
    })

@app.route('/api/books', methods=['GET'])
def get_books():
    """Dapatkan semua buku dengan pagination"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    
    start = (page - 1) * limit
    end = start + limit
    
    books = BOOKS_DATA[start:end]
    
    return jsonify({
        "success": True,
        "total": len(BOOKS_DATA),
        "page": page,
        "limit": limit,
        "data": books
    })

@app.route('/api/books/search', methods=['GET'])
def search_books():
    """Cari buku"""
    query = request.args.get('q', '', type=str).lower()
    
    if not query:
        return jsonify({
            "success": False,
            "message": "Parameter 'q' diperlukan"
        }), 400
    
    results = [book for book in BOOKS_DATA if query in book["name"].lower()]
    
    return jsonify({
        "success": True,
        "query": query,
        "total": len(results),
        "data": results
    })

@app.route('/api/books/filter', methods=['GET'])
def filter_books():
    """Filter buku berdasarkan ukuran"""
    size_filter = request.args.get('size', '', type=str).lower()
    folder = request.args.get('folder', '', type=str)
    
    if size_filter not in ['small', 'medium', 'large', '']:
        return jsonify({
            "success": False,
            "message": "Size harus: small, medium, atau large"
        }), 400
    
    results = BOOKS_DATA
    
    if size_filter:
        results = [book for book in results if get_size_category(book["size"]) == size_filter]
    
    if folder:
        results = [book for book in results if book["folder"].lower() == folder.lower()]
    
    return jsonify({
        "success": True,
        "filter": {
            "size": size_filter if size_filter else "all",
            "folder": folder if folder else "all"
        },
        "total": len(results),
        "data": results
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Dapatkan statistik"""
    stats = calculate_stats()
    
    # Kategori ukuran
    size_breakdown = {
        "small": len([b for b in BOOKS_DATA if get_size_category(b["size"]) == "small"]),
        "medium": len([b for b in BOOKS_DATA if get_size_category(b["size"]) == "medium"]),
        "large": len([b for b in BOOKS_DATA if get_size_category(b["size"]) == "large"])
    }
    
    # Breakdown per folder
    folder_breakdown = {}
    for book in BOOKS_DATA:
        folder = book["folder"]
        if folder not in folder_breakdown:
            folder_breakdown[folder] = {"count": 0, "total_size": 0}
        folder_breakdown[folder]["count"] += 1
        folder_breakdown[folder]["total_size"] += book["size"]
    
    # Round sizes
    for folder in folder_breakdown:
        folder_breakdown[folder]["total_size"] = round(folder_breakdown[folder]["total_size"], 2)
    
    return jsonify({
        "success": True,
        "stats": stats,
        "size_distribution": size_breakdown,
        "folder_distribution": folder_breakdown
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Dapatkan kategori unik dari nama buku"""
    categories = set()
    
    keywords = ["Hybrid", "Electric", "ADAS", "ECU", "Engine", "Diesel", "Bosch", 
                "Toyota", "Honda", "Suzuki", "Mitsubishi", "Daihatsu", "Hyundai",
                "CAN", "OBD", "Wiring", "Service", "Manual", "Training"]
    
    category_count = {}
    for keyword in keywords:
        count = len([b for b in BOOKS_DATA if keyword.lower() in b["name"].lower()])
        if count > 0:
            category_count[keyword] = count
    
    return jsonify({
        "success": True,
        "categories": sorted(category_count.items(), key=lambda x: x[1], reverse=True)
    })

@app.route('/api/folders', methods=['GET'])
def get_folders():
    """Dapatkan daftar folder"""
    folders = list(set(book["folder"] for book in BOOKS_DATA))
    return jsonify({
        "success": True,
        "folders": folders
    })

@app.route('/api/download-link', methods=['GET'])
def get_download_link():
    """Dapatkan link download file"""
    folder = request.args.get('folder', 'EBOOKS', type=str)
    filename = request.args.get('file', '', type=str)
    
    if not filename:
        return jsonify({
            "success": False,
            "message": "Parameter 'file' diperlukan"
        }), 400
    
    # Verify file exists
    file_found = any(book["name"] == filename and book["folder"] == folder for book in BOOKS_DATA)
    
    if not file_found:
        return jsonify({
            "success": False,
            "message": "File tidak ditemukan"
        }), 404
    
    return jsonify({
        "success": True,
        "download_url": f"http://localhost:8000/{folder}/{filename}",
        "file": filename,
        "folder": folder
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "ok",
        "message": "API running"
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "message": "Endpoint tidak ditemukan. Kunjungi /api untuk melihat dokumentasi."
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Perpustakaan E-Books API Server")
    print("=" * 60)
    print("\n📍 API berjalan di: http://localhost:5000")
    print("\n📚 Dokumentasi API:")
    print("   - http://localhost:5000/api")
    print("\n💡 Contoh penggunaan:")
    print("   - http://localhost:5000/api/books")
    print("   - http://localhost:5000/api/books/search?q=hybrid")
    print("   - http://localhost:5000/api/books/filter?size=large")
    print("   - http://localhost:5000/api/stats")
    print("   - http://localhost:5000/api/categories")
    print("\n✅ CORS enabled - dapat diakses dari web lain")
    print("\n🛑 Tekan Ctrl+C untuk menghentikan server\n")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
