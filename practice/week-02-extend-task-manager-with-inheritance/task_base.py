"""
task_base module defining the TaskBase hierarchy for the Task Management System.

Demonstrates Object-Oriented Programming (OOP) inheritance principles:
- Base class: TaskBase
- Derived subclasses: Task (standard), UrgentTask, RecurringTask
"""
from typing import Optional, Dict, Any, Type, List


class TaskBase:
    """
    Base class representing a general task.

    Attributes:
        title (str): The title of the task (must be non-empty).
        description (str): A detailed description of the task.
        status (str): Current status ('Pending', 'In Progress', 'Completed').
    """

    VALID_STATUSES = ["Pending", "In Progress", "Completed"]
    _subclasses: Dict[str, Type["TaskBase"]] = {}

    def __init_subclass__(cls, **kwargs):
        """Automatically register subclasses for polymorphic deserialization."""
        super().__init_subclass__(**kwargs)
        cls._subclasses[cls.__name__] = cls

    def __init__(self, title: str, description: str = "", status: str = "Pending") -> None:
        """
        Initialize a new TaskBase instance.

        Args:
            title: Title of the task (non-empty string).
            description: Optional descriptive text.
            status: Task status (default 'Pending').

        Raises:
            ValueError: If title is empty or whitespace-only.
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty.")

        self.title: str = title.strip()
        self.description: str = description.strip() if description else ""
        self.status: str = self._validate_status(status)

    @classmethod
    def _validate_status(cls, status: str) -> str:
        """Normalize and validate the task status."""
        normalized = status.strip().title()
        if normalized in cls.VALID_STATUSES:
            return normalized
        return status.strip()

    def update_status(self, new_status: str) -> None:
        """Update the task status to a new validated status."""
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

    def get_details(self) -> str:
        """Return formatted string containing detailed task info."""
        desc = f" | Description: {self.description}" if self.description else ""
        return f"[{self.__class__.__name__}] {self.title} (Status: {self.status}){desc}"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize base task attributes into a dictionary."""
        return {
            "task_type": self.__class__.__name__,
            "title": self.title,
            "description": self.description,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskBase":
        """
        Polymorphically reconstruct a task instance from a dictionary.

        Detects 'task_type' in the dictionary to instantiate the correct subclass.
        """
        task_type = data.get("task_type", cls.__name__)
        target_cls = cls._subclasses.get(task_type, cls)

        if target_cls is not cls and issubclass(target_cls, TaskBase):
            return target_cls.from_dict(data)

        return cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            status=data.get("status", "Pending"),
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(title='{self.title}', status='{self.status}')"

    def __str__(self) -> str:
        desc = f" - {self.description}" if self.description else ""
        return f"[{self.status}] {self.title}{desc}"


class Task(TaskBase):
    """
    Standard Task implementation inheriting directly from TaskBase.
    Maintains backward compatibility with earlier Task Manager versions.
    """
    pass


class UrgentTask(TaskBase):
    """
    Specialized task subclass for time-sensitive or high-priority tasks.

    Inherits from TaskBase and adds urgency level and deadline handling.
    """

    VALID_URGENCY_LEVELS = ["Low", "Medium", "High", "Critical"]

    def __init__(
        self,
        title: str,
        description: str = "",
        status: str = "Pending",
        urgency_level: str = "High",
        deadline: Optional[str] = None,
    ) -> None:
        """
        Initialize an UrgentTask instance.

        Args:
            title: Title of the urgent task.
            description: Optional description.
            status: Status (default 'Pending').
            urgency_level: Urgency tier ('Low', 'Medium', 'High', 'Critical').
            deadline: Optional deadline string (e.g., '2026-10-01' or 'Today 5pm').
        """
        super().__init__(title=title, description=description, status=status)
        self.urgency_level: str = self._validate_urgency(urgency_level)
        self.deadline: Optional[str] = deadline.strip() if deadline else None

    @classmethod
    def _validate_urgency(cls, level: str) -> str:
        """Validate and normalize urgency level."""
        normalized = level.strip().title()
        if normalized in cls.VALID_URGENCY_LEVELS:
            return normalized
        return "High"

    def escalate_urgency(self, new_level: Optional[str] = None) -> None:
        """
        Escalate the urgency level of the task.
        If new_level is provided, sets to that level; otherwise steps up to next level.
        """
        if new_level:
            self.urgency_level = self._validate_urgency(new_level)
            return

        current_idx = self.VALID_URGENCY_LEVELS.index(self.urgency_level)
        if current_idx < len(self.VALID_URGENCY_LEVELS) - 1:
            self.urgency_level = self.VALID_URGENCY_LEVELS[current_idx + 1]

    def is_critical(self) -> bool:
        """Check if the task has reached Critical urgency."""
        return self.urgency_level == "Critical"

    def get_details(self) -> str:
        """Override get_details to emphasize urgency and deadline."""
        base_details = super().get_details()
        deadline_str = f" | Deadline: {self.deadline}" if self.deadline else " | Deadline: None"
        return f"{base_details} | Urgency: {self.urgency_level}{deadline_str}"

    def to_dict(self) -> Dict[str, Any]:
        """Override to_dict to serialize urgency attributes."""
        data = super().to_dict()
        data.update({
            "urgency_level": self.urgency_level,
            "deadline": self.deadline,
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UrgentTask":
        """Reconstruct an UrgentTask from a dictionary."""
        return cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            status=data.get("status", "Pending"),
            urgency_level=data.get("urgency_level", "High"),
            deadline=data.get("deadline"),
        )

    def __str__(self) -> str:
        """Override string representation with urgent banner and deadline."""
        deadline_info = f" [Due: {self.deadline}]" if self.deadline else ""
        desc = f" - {self.description}" if self.description else ""
        return f"[URGENT - {self.urgency_level}] [{self.status}] {self.title}{deadline_info}{desc}"


class RecurringTask(TaskBase):
    """
    Specialized task subclass for tasks that repeat on a regular schedule.

    Inherits from TaskBase and overrides completion behavior to support
    automatic cycle recurrence.
    """

    VALID_FREQUENCIES = ["Daily", "Weekly", "Bi-Weekly", "Monthly", "Quarterly", "Yearly"]

    def __init__(
        self,
        title: str,
        description: str = "",
        status: str = "Pending",
        frequency: str = "Weekly",
        interval: int = 1,
        completed_occurrences: int = 0,
        max_occurrences: Optional[int] = None,
    ) -> None:
        """
        Initialize a RecurringTask instance.

        Args:
            title: Title of the recurring task.
            description: Optional description.
            status: Status (default 'Pending').
            frequency: Recurrence interval unit ('Daily', 'Weekly', etc.).
            interval: Step interval (e.g., 2 for every 2 weeks).
            completed_occurrences: Number of recurring cycles completed so far.
            max_occurrences: Optional cap on how many times task repeats.
        """
        super().__init__(title=title, description=description, status=status)
        self.frequency: str = self._validate_frequency(frequency)
        self.interval: int = max(1, int(interval))
        self.completed_occurrences: int = max(0, int(completed_occurrences))
        self.max_occurrences: Optional[int] = max_occurrences if (max_occurrences is None or max_occurrences > 0) else None

    @classmethod
    def _validate_frequency(cls, freq: str) -> str:
        """Validate and normalize recurrence frequency."""
        normalized = freq.strip().title()
        for valid in cls.VALID_FREQUENCIES:
            if valid.lower() == normalized.lower():
                return valid
        return "Weekly"

    def mark_completed(self, auto_renew: bool = True) -> bool:
        """
        Override mark_completed to handle recurring task cycle renewal.

        Args:
            auto_renew: If True and max_occurrences is not reached, increments
                        completed cycles and resets status back to 'Pending'.

        Returns:
            bool: True if permanently completed, False if renewed for next cycle.
        """
        self.completed_occurrences += 1

        if self.max_occurrences is not None and self.completed_occurrences >= self.max_occurrences:
            self.status = "Completed"
            return True

        if auto_renew:
            self.status = "Pending"
            return False
        else:
            self.status = "Completed"
            return True

    def renew_cycle(self) -> None:
        """Manually trigger a cycle advance and reset status to Pending."""
        self.completed_occurrences += 1
        if self.max_occurrences is not None and self.completed_occurrences >= self.max_occurrences:
            self.status = "Completed"
        else:
            self.status = "Pending"

    def has_finished_all_occurrences(self) -> bool:
        """Check if all planned occurrences have been completed."""
        if self.max_occurrences is None:
            return False
        return self.completed_occurrences >= self.max_occurrences

    def get_details(self) -> str:
        """Override get_details to display recurrence cycle metrics."""
        base_details = super().get_details()
        max_str = f"/{self.max_occurrences}" if self.max_occurrences else ""
        return (
            f"{base_details} | Recurrence: Every {self.interval} {self.frequency} "
            f"| Completed Cycles: {self.completed_occurrences}{max_str}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Override to_dict to serialize recurring task attributes."""
        data = super().to_dict()
        data.update({
            "frequency": self.frequency,
            "interval": self.interval,
            "completed_occurrences": self.completed_occurrences,
            "max_occurrences": self.max_occurrences,
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecurringTask":
        """Reconstruct a RecurringTask from a dictionary."""
        return cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            status=data.get("status", "Pending"),
            frequency=data.get("frequency", "Weekly"),
            interval=data.get("interval", 1),
            completed_occurrences=data.get("completed_occurrences", 0),
            max_occurrences=data.get("max_occurrences"),
        )

    def __str__(self) -> str:
        """Override string representation to include recurrence frequency and cycle count."""
        max_str = f"/{self.max_occurrences}" if self.max_occurrences else ""
        desc = f" - {self.description}" if self.description else ""
        return f"[RECURRING - {self.frequency}] [{self.status}] {self.title} (Cycles: {self.completed_occurrences}{max_str}){desc}"
