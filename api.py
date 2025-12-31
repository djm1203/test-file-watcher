"""HTTP API handlers for the task service."""

import json
from http.server import BaseHTTPRequestHandler
from typing import Tuple
from service import TaskService
from models import TaskStatus


class TaskApiHandler(BaseHTTPRequestHandler):
    """HTTP handler for task API."""

    service: TaskService = None  # Set by main

    def send_json(self, data: dict, status: int = 200) -> None:
        """Send JSON response."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict:
        """Read JSON from request body."""
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        return json.loads(body) if body else {}

    def parse_path(self) -> Tuple[str, int]:
        """Parse path into (resource, id)."""
        parts = self.path.strip("/").split("/")
        resource = parts[0] if parts else ""
        id_val = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        return resource, id_val

    def do_GET(self) -> None:
        """Handle GET requests."""
        resource, task_id = self.parse_path()

        if resource == "health":
            self.send_json({"status": "healthy", "tasks": self.service.count()})
        elif resource == "tasks" and task_id:
            task = self.service.get(task_id)
            if task:
                self.send_json(task.to_dict())
            else:
                self.send_json({"error": "Task not found"}, 404)
        elif resource == "tasks":
            tasks = self.service.list_all()
            self.send_json({"tasks": [t.to_dict() for t in tasks]})
        else:
            self.send_json({"error": "Not found"}, 404)

    def do_POST(self) -> None:
        """Handle POST requests."""
        resource, _ = self.parse_path()

        if resource == "tasks":
            data = self.read_json()
            title = data.get("title", "")
            desc = data.get("description", "")
            if not title:
                self.send_json({"error": "Title required"}, 400)
                return
            task = self.service.create(title, desc)
            self.send_json(task.to_dict(), 201)
        else:
            self.send_json({"error": "Not found"}, 404)

    def do_DELETE(self) -> None:
        """Handle DELETE requests."""
        resource, task_id = self.parse_path()

        if resource == "tasks" and task_id:
            if self.service.delete(task_id):
                self.send_json({"deleted": True})
            else:
                self.send_json({"error": "Task not found"}, 404)
        else:
            self.send_json({"error": "Not found"}, 404)
