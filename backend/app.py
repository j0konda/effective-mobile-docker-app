#!/usr/bin/env python3
"""Simple HTTP server for Effective Mobile test task."""

from http.server import HTTPServer, BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    """Handle GET requests."""

    def do_GET(self):  # noqa: N802
        """Process GET request."""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Hello from Effective Mobile!')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

    def log_message(self, format, *args):  # noqa: A002
        """Suppress default logging to keep logs clean."""
        pass


if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', 8080
    server = HTTPServer((HOST, PORT), RequestHandler)
    print(f'Starting backend server on {HOST}:{PORT}...')
    server.serve_forever()