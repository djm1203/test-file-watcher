"""Task service with business logic."""

from typing import List, Optional
from models import Task, TaskStatus, create_task


class TaskService:
    """Service for managing tasks."""

    def __init__(self):
        """Initialize with empty task storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def create(self, title: str, description: str) -> Task:
        """Create a new task."""
        task = create_task(self._next_id, title, description)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        return self._tasks.get(task_id)

    def list_all(self) -> List[Task]:
        """List all tasks."""
        return list(self._tasks.values())

    def list_by_status(self, status: TaskStatus) -> List[Task]:
        """List tasks filtered by status."""
        return [t for t in self._tasks.values() if t.status == status]

    def update_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        """Update task status."""
        task = self._tasks.get(task_id)
        if task:
            if status == TaskStatus.COMPLETED:
                task.mark_complete()
            elif status == TaskStatus.IN_PROGRESS:
                task.mark_in_progress()
            else:
                task.status = status
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task. Returns True if deleted."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def count(self) -> int:
        """Get total task count."""
        return len(self._tasks)

    def count_by_status(self, status: TaskStatus) -> int:
        """Count tasks by status."""
        return len([t for t in self._tasks.values() if t.status == status])
