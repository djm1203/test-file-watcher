"""Data models for the task service."""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task:
    """Represents a task."""
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def mark_complete(self) -> None:
        """Mark task as completed."""
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.now()

    def mark_in_progress(self) -> None:
        """Mark task as in progress."""
        self.status = TaskStatus.IN_PROGRESS
        self.updated_at = datetime.now()


def create_task(id: int, title: str, description: str) -> Task:
    """Factory function to create a new task."""
    return Task(
        id=id,
        title=title,
        description=description,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
