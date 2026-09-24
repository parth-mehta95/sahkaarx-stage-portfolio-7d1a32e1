"""
Project module defining the Project class that composes Task instances without inheritance.
"""
from typing import List, Optional, Dict, Any
from task import Task


class Project:
    """
    Represents a project containing a collection of tasks.

    Demonstrates composition over inheritance: A Project 'has-a' list of Task instances
    rather than inheriting from Task.
    """

    def __init__(self, name: str, description: str = "") -> None:
        """
        Initialize a new Project instance.

        Args:
            name: The name or title of the project.
            description: Optional details about the project.

        Raises:
            ValueError: If project name is empty or whitespace-only.
        """
        if not name or not name.strip():
            raise ValueError("Project name cannot be empty.")

        self.name: str = name.strip()
        self.description: str = description.strip() if description else ""
        self._tasks: List[Task] = []

    @property
    def tasks(self) -> List[Task]:
        """Return a copy of the list of tasks to preserve encapsulation."""
        return list(self._tasks)

    def add_task(self, task: Task) -> None:
        """
        Add a Task instance to this project.

        Args:
            task: An instance of Task.

        Raises:
            TypeError: If the argument is not an instance of Task.
            ValueError: If a task with the same title already exists.
        """
        if not isinstance(task, Task):
            raise TypeError(f"Expected Task instance, got {type(task).__name__}")

        if any(existing.title.lower() == task.title.lower() for existing in self._tasks):
            raise ValueError(f"Task with title '{task.title}' already exists in project '{self.name}'.")

        self._tasks.append(task)

    def remove_task(self, title: str) -> bool:
        """
        Remove a task by its title (case-insensitive).

        Args:
            title: The title of the task to remove.

        Returns:
            True if task was found and removed, False otherwise.
        """
        initial_len = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.title.lower() != title.strip().lower()]
        return len(self._tasks) < initial_len

    def get_task(self, title: str) -> Optional[Task]:
        """
        Retrieve a task by its title (case-insensitive).

        Args:
            title: The title of the task to look up.

        Returns:
            The Task instance if found, or None.
        """
        target = title.strip().lower()
        for task in self._tasks:
            if task.title.lower() == target:
                return task
        return None

    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        """
        List all tasks or filter tasks by status.

        Args:
            status: Optional status to filter by (e.g. 'Pending', 'Completed').

        Returns:
            List of matching Task instances.
        """
        if not status:
            return list(self._tasks)
        normalized = status.strip().lower()
        return [t for t in self._tasks if t.status.lower() == normalized]

    def total_tasks(self) -> int:
        """Return total number of tasks in project."""
        return len(self._tasks)

    def completed_tasks(self) -> int:
        """Return count of completed tasks."""
        return sum(1 for t in self._tasks if t.is_completed())

    def pending_tasks(self) -> int:
        """Return count of pending tasks."""
        return sum(1 for t in self._tasks if not t.is_completed())

    def to_dict(self) -> Dict[str, Any]:
        """Serialize project and its composed tasks into a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "tasks": [task.to_dict() for task in self._tasks],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """
        Create a Project instance from a dictionary, reconstructing composed Task instances.

        Args:
            data: Dictionary containing 'name', 'description', and 'tasks'.
        """
        project = cls(
            name=data.get("name", "Default Project"),
            description=data.get("description", ""),
        )
        for task_data in data.get("tasks", []):
            project.add_task(Task.from_dict(task_data))
        return project

    def __repr__(self) -> str:
        return f"Project(name='{self.name}', tasks_count={len(self._tasks)})"

    def __str__(self) -> str:
        header = f"Project: {self.name}"
        if self.description:
            header += f" ({self.description})"
        header += f" [{self.completed_tasks()}/{self.total_tasks()} completed]"
        if not self._tasks:
            return f"{header}\n  (No tasks)"
        task_lines = "\n".join(f"  - {task}" for task in self._tasks)
        return f"{header}\n{task_lines}"
