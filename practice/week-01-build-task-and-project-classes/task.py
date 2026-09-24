"""
Task module defining the Task class for the Task Management CLI.
"""
from typing import Optional, Dict, Any


class Task:
    """
    Represents an individual task with a title, description, and status.

    Attributes:
        title (str): The title or name of the task.
        description (str): A detailed description of the task.
        status (str): Current status of the task (e.g., 'Pending', 'In Progress', 'Completed').
    """

    VALID_STATUSES = ["Pending", "In Progress", "Completed"]

    def __init__(self, title: str, description: str = "", status: str = "Pending") -> None:
        """
        Initialize a new Task instance.

        Args:
            title: The title of the task (must be non-empty).
            description: Optional details about the task.
            status: Initial status of the task (defaults to 'Pending').

        Raises:
            ValueError: If title is empty or whitespace-only.
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty.")

        self.title: str = title.strip()
        self.description: str = description.strip() if description else ""
        self.status: str = self._validate_status(status)

    def _validate_status(self, status: str) -> str:
        """Normalize and validate the task status."""
        normalized = status.strip().title()
        if normalized in self.VALID_STATUSES:
            return normalized
        return status.strip()

    def update_status(self, new_status: str) -> None:
        """
        Update the status of the task.

        Args:
            new_status: The new status string to set.
        """
        self.status = self._validate_status(new_status)

    def mark_completed(self) -> None:
        """Mark the task as Completed."""
        self.status = "Completed"

    def mark_in_progress(self) -> None:
        """Mark the task as In Progress."""
        self.status = "In Progress"

    def mark_pending(self) -> None:
        """Mark the task as Pending."""
        self.status = "Pending"

    def is_completed(self) -> bool:
        """Check if the task is completed."""
        return self.status.lower() == "completed"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the task to a dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """
        Create a Task instance from a dictionary.

        Args:
            data: Dictionary containing 'title', 'description', and 'status'.
        """
        return cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            status=data.get("status", "Pending"),
        )

    def __repr__(self) -> str:
        return f"Task(title='{self.title}', status='{self.status}')"

    def __str__(self) -> str:
        desc = f" - {self.description}" if self.description else ""
        return f"[{self.status}] {self.title}{desc}"
