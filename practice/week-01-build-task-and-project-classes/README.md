# Task Manager CLI

A lightweight, robust command-line task management application built in Python. Designed using clean Object-Oriented Programming (OOP) principles, emphasizing **composition over inheritance** to structure `Task` and `Project` models.

---

## Table of Contents

- [Overview](#overview)
- [Class Design & Architecture](#class-design--architecture)
  - [Composition vs. Inheritance](#composition-vs-inheritance)
  - [The `Task` Class (`task.py`)](#the-task-class-taskpy)
  - [The `Project` Class (`project.py`)](#the-project-class-projectpy)
- [How to Run the CLI](#how-to-run-the-cli)
  - [Prerequisites](#prerequisites)
  - [Command-Line Arguments](#command-line-arguments)
  - [Interactive Mode](#interactive-mode)
- [Programmatic Usage](#programmatic-usage)
- [Running Unit Tests](#running-unit-tests)
- [Project Structure](#project-structure)

---

## Overview

The **Task Manager CLI** provides a foundation for organizing and tracking tasks grouped within projects. It supports in-memory manipulation as well as JSON file persistence (`tasks.json`).

Key Highlights:
- **Zero External Dependencies**: Built strictly using Python's standard library (`argparse`, `json`, `unittest`).
- **Composition-First Design**: Projects maintain and manage tasks via reference composition rather than rigid class inheritance.
- **Dual Interface**: Operate seamlessly via direct CLI subcommands or an intuitive interactive console menu.

---

## Class Design & Architecture

### Composition vs. Inheritance

A foundational principle in object-oriented design is **"Favor object composition over class inheritance"**.

- **Why NOT Inheritance?**
  - A `Project` is **not** a `Task` (it fails the "is-a" test). Making `Project` inherit from `Task` would force it to adopt fields like `status` or single-task completion semantics that make no conceptual sense for an entire container of tasks.
  - Similarly, a `Task` is not a `Project`.
  - Inheritance creates tight coupling: changes to the parent class risk breaking child class behavior.

- **Why Composition?**
  - A `Project` **has** tasks (a "has-a" relationship).
  - The `Project` class encapsulates a collection of `Task` instances in its private `_tasks` list.
  - High cohesion & loose coupling: `Task` only cares about task-level attributes (`title`, `description`, `status`), while `Project` orchestrates task collections, filtering, counting, and lookups.

```
+------------------------------------------+
|                 Project                  |
+------------------------------------------+
| - name: str                              |
| - description: str                       |
| - _tasks: List[Task]                     |
+------------------------------------------+
| + add_task(task: Task) -> None           |
| + remove_task(title: str) -> bool        |
| + get_task(title: str) -> Optional[Task] |
| + list_tasks(status: str) -> List[Task]  |
| + total_tasks() -> int                   |
| + completed_tasks() -> int               |
+------------------------------------------+
                     |
                     | 1..* (composes)
                     v
+------------------------------------------+
|                  Task                    |
+------------------------------------------+
| - title: str                             |
| - description: str                       |
| - status: str                            |
+------------------------------------------+
| + update_status(status: str) -> None     |
| + mark_completed() -> None               |
| + is_completed() -> bool                 |
| + to_dict() -> Dict[str, Any]            |
+------------------------------------------+
```

---

### The `Task` Class (`task.py`)

Stores individual task state and behavior:
- **`title`**: String representing the task summary (cannot be empty).
- **`description`**: Optional detailed description string.
- **`status`**: String indicating state (e.g. `Pending`, `In Progress`, `Completed`).
- **Methods**:
  - `update_status(new_status)`: Updates and normalizes task status.
  - `mark_completed()`, `mark_in_progress()`, `mark_pending()`: Convenience status mutators.
  - `is_completed()`: Returns boolean indicating completion.
  - `to_dict()`, `from_dict(data)`: Serialization helpers.

---

### The `Project` Class (`project.py`)

Manages a collection of tasks using composition:
- **`name`**: Project name / title.
- **`description`**: Optional project context.
- **`tasks`**: Read-only property returning a copy of the task list to safeguard encapsulation.
- **Methods**:
  - `add_task(task)`: Appends a `Task` instance (prevents duplicate titles and type mismatches).
  - `remove_task(title)`: Removes task by title (case-insensitive).
  - `get_task(title)`: Finds and returns a `Task` instance by title.
  - `list_tasks(status=None)`: Returns all tasks or tasks filtered by status.
  - `total_tasks()`, `completed_tasks()`, `pending_tasks()`: Summary counters.
  - `to_dict()`, `from_dict(data)`: Serializes/deserializes project and nested tasks.

---

## How to Run the CLI

### Prerequisites
- Python 3.8+ (tested on Python 3.11)

### Command-Line Arguments

#### 1. Add a Task
```bash
python cli.py add "Setup Git Repository" -d "Initialize repository on GitHub" -s "Completed"
python cli.py add "Build Task class" -d "Implement title, description, and status" -s "Completed"
python cli.py add "Build Project class" -d "Compose Task instances" -s "In Progress"
```

#### 2. List Tasks
List all tasks:
```bash
python cli.py list
```

Filter tasks by status:
```bash
python cli.py list -s Completed
python cli.py list -s "In Progress"
python cli.py list -s Pending
```

#### 3. Mark a Task as Completed
```bash
python cli.py complete "Build Project class"
```

#### 4. Remove a Task
```bash
python cli.py remove "Setup Git Repository"
```

---

### Interactive Mode

Run the CLI without arguments or with `interactive` to enter the interactive console menu:

```bash
python cli.py
# or
python cli.py interactive
```

Menu options:
```text
==============================
    TASK MANAGER CLI
==============================
1. List all tasks
2. Add a new task
3. Mark task as Completed
4. Remove a task
5. Exit
Enter choice (1-5):
```

---

## Programmatic Usage

You can also import and use `Task` and `Project` in your own Python scripts:

```python
from task import Task
from project import Project

# Initialize a project
project = Project(name="Q1 Product Launch", description="Tasks for product release")

# Create tasks
t1 = Task(title="Market Research", description="Survey top 50 beta users")
t2 = Task(title="Deploy Backend", status="In Progress")

# Compose tasks into project
project.add_task(t1)
project.add_task(t2)

# Query and update
t1.mark_completed()

print(project)
# Output:
# Project: Q1 Product Launch (Tasks for product release) [1/2 completed]
#   - [Completed] Market Research - Survey top 50 beta users
#   - [In Progress] Deploy Backend
```

---

## Running Unit Tests

Comprehensive unit tests are provided in `test_task_manager.py`:

```bash
python -m unittest test_task_manager.py
```

Test coverage includes:
- Task attribute persistence and validation
- Status transitions and helper methods
- Verification that `Project` does not inherit from `Task`
- Project composition, task management, duplicate prevention, and filtering
- JSON serialization / deserialization roundtrip

---

## Project Structure

```text
task-manager-cli/
├── README.md               # Documentation and architecture guide
├── task.py                 # Task class definition
├── project.py              # Project class definition (composition)
├── cli.py                  # CLI and interactive console entry point
└── test_task_manager.py    # Unit tests suite
```