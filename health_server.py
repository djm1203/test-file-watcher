#!/usr/bin/env python3
"""
Minimal HTTP health check server.
Runs continuously, responds to /health with JSON status.
"""

import json
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8080"))

START_TIME = time.time()


class HealthHandler(BaseHTTPRequestHandler):
    """Handle HTTP requests."""

    def log_message(self, format, *args):
        """Override to print cleaner logs."""
        print(f"[{self.command}] {self.path} - {args[1]}")

    def send_json(self, data: dict, status: int = 200):
        """Send JSON response."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/health":
            uptime = int(time.time() - START_TIME)
            self.send_json({
                "status": "healthy",
                "uptime_seconds": uptime,
                "service": "health-server"
            })
        elif self.path == "/":
            self.send_json({
                "message": "Hello from health-server!",
                "endpoints": ["/", "/health", "/echo"]
            })
        elif self.path == "/echo":
            self.send_json({
                "method": self.command,
                "path": self.path,
                "headers": dict(self.headers)
            })
        else:
            self.send_json({"error": "Not found"}, 404)

    def do_POST(self):
        """Handle POST requests."""
        if self.path == "/echo":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            self.send_json({
                "method": self.command,
                "path": self.path,
                "body": body,
                "headers": dict(self.headers)
            })
        else:
            self.send_json({"error": "Not found"}, 404)


def main():
    print(f"Health Server starting...")
    print(f"Listening on {HOST}:{PORT}")
    print(f"Endpoints: /, /health, /echo")

    server = HTTPServer((HOST, PORT), HealthHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
