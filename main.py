"""Main entry point for the task service."""

import os
from http.server import HTTPServer
from service import TaskService
from api import TaskApiHandler


def main() -> None:
    """Start the task service HTTP server."""
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8080"))

    # Initialize service
    service = TaskService()
    TaskApiHandler.service = service

    print(f"Task Service starting...")
    print(f"Listening on {host}:{port}")
    print(f"Endpoints: /health, /tasks, /tasks/<id>")

    server = HTTPServer((host, port), TaskApiHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
