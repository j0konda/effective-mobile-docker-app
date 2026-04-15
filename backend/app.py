#!/usr/bin/env python3
import os
import signal
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            self.wfile.write(b'Hello from Effective Mobile!')
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"healthy","timestamp":"' + 
                           datetime.now().isoformat().encode() + b'"}')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def do_HEAD(self):
        # Обрабатываем HEAD так же, как GET, но без тела ответа
        if self.path == '/' or self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', len('Hello from Effective Mobile!'))
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()    

    def log_message(self, format, *args):
        # Кастомное логирование с временем
        print(f"[{datetime.now().isoformat()}] {self.address_string()} - {format % args}")

def signal_handler(signum, frame):
    print(f"Received signal {signum}, shutting down...")
    sys.exit(0)

if __name__ == '__main__':
    # Обработка сигналов для graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    server = HTTPServer(('0.0.0.0', 8080), Handler)
    print(f'Backend server running on port 8080 (PID: {os.getpid()})')
    print('Health check available at /health')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Server shutdown complete")