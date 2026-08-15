"""
server.py
---------
Python HTTP Server untuk melayani Interactive Web Visualizer Dashboard.
"""

import http.server
import socketserver
import os
import sys

PORT = 5000

class VisualizerHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Always serve from web_visualizer directory
        directory = os.path.dirname(os.path.abspath(__file__))
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format, *args):
        # Clean logging format
        sys.stdout.write("[%s] %s\n" % (self.log_date_time_string(), format % args))

def start_server():
    Handler = VisualizerHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("\n" + "=" * 60)
        print(" 🌐 LLM EVALUATIONS INTERACTIVE WEB VISUALIZER DASHBOARD")
        print("=" * 60)
        print(f"  Status    : Running 🚀")
        print(f"  URL       : http://localhost:{PORT}")
        print(f"  Directory : {os.path.dirname(os.path.abspath(__file__))}")
        print("  Tekan Ctrl+C untuk menghentikan server.")
        print("=" * 60 + "\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer dihentikan oleh pengguna. Sampai jumpa! 👋")
            httpd.server_close()

if __name__ == "__main__":
    start_server()
