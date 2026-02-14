#!/usr/bin/env python3
"""
Simple HTTP Server untuk melayani halaman Perpustakaan E-Books
"""
import http.server
import socketserver
import os
import sys
from pathlib import Path

PORT = 8000
DIRECTORY = "/workspaces/ebooks"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        super().end_headers()

def run_server():
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"✅ Server berjalan!")
        print(f"📍 Buka browser ke: http://localhost:{PORT}")
        print(f"📁 Direktori: {DIRECTORY}")
        print(f"\n💡 Tekan Ctrl+C untuk menghentikan server\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n❌ Server dihentikan")
            sys.exit(0)

if __name__ == "__main__":
    run_server()
