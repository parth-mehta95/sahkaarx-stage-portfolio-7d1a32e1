"""
Command-Line Interface (CLI) for Task Management.
Allows creating, listing, and updating tasks managed within a Project.
"""
import argparse
import json
import os
import sys
from typing import Optional

from task import Task
from project import Project

DEFAULT_STORAGE_FILE = "tasks.json"


def load_project(filepath: str = DEFAULT_STORAGE_FILE) -> Project:
    """Load project and tasks from a JSON file, or return a default project."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return Project.from_dict(data)
        except (json.JSONDecodeError, IOError, ValueError) as e:
            print(f"[Warning] Failed to read {filepath} ({e}). Starting with a new project.")
    return Project(name="Default Project", description="General workspace tasks")


def save_project(project: Project, filepath: str = DEFAULT_STORAGE_FILE) -> None:
    """Save the project and its tasks to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(project.to_dict(), f, indent=2)


def cmd_add(project: Project, title: str, description: str, status: str, storage_file: str) -> None:
    """Add a new task to the project and persist."""
    try:
        task = Task(title=title, description=description, status=status)
        project.add_task(task)
        save_project(project, storage_file)
        print(f"[+] Task added successfully: '{task.title}' [{task.status}]")
    except (ValueError, TypeError) as err:
        print(f"[-] Error adding task: {err}")


def cmd_list(project: Project, status_filter: Optional[str] = None) -> None:
    """List tasks, optionally filtered by status."""
    tasks = project.list_tasks(status=status_filter)
    filter_label = f" (filtered by status='{status_filter}')" if status_filter else ""
    print(f"\n--- Project: {project.name}{filter_label} ---")
    if not tasks:
        print("  No tasks found.")
    else:
        for idx, task in enumerate(tasks, start=1):
            desc_part = f" - {task.description}" if task.description else ""
            print(f"  {idx}. [{task.status}] {task.title}{desc_part}")
    print(f"Total: {len(tasks)} task(s)\n")


def cmd_complete(project: Project, title: str, storage_file: str) -> None:
    """Mark a task as completed and persist."""
    task = project.get_task(title)
    if not task:
        print(f"[-] Task '{title}' not found.")
        return
    task.mark_completed()
    save_project(project, storage_file)
    print(f"[+] Task '{task.title}' marked as Completed.")


def cmd_remove(project: Project, title: str, storage_file: str) -> None:
    """Remove a task from the project and persist."""
    if project.remove_task(title):
        save_project(project, storage_file)
        print(f"[+] Task '{title}' removed.")
    else:
        print(f"[-] Task '{title}' not found.")


def interactive_menu(project: Project, storage_file: str) -> None:
    """Run an interactive console menu."""
    while True:
        print("\n==============================")
        print("    TASK MANAGER CLI")
        print("==============================")
        print("1. List all tasks")
        print("2. Add a new task")
        print("3. Mark task as Completed")
        print("4. Remove a task")
        print("5. Exit")
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            filter_choice = input("Filter by status (leave empty for all): ").strip()
            cmd_list(project, filter_choice or None)
        elif choice == "2":
            title = input("Enter task title: ").strip()
            if not title:
                print("Title cannot be empty.")
                continue
            desc = input("Enter description (optional): ").strip()
            status = input("Enter status [Pending / In Progress / Completed] (default: Pending): ").strip() or "Pending"
            cmd_add(project, title, desc, status, storage_file)
        elif choice == "3":
            title = input("Enter title of task to complete: ").strip()
            cmd_complete(project, title, storage_file)
        elif choice == "4":
            title = input("Enter title of task to remove: ").strip()
            cmd_remove(project, title, storage_file)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-5.")


def main() -> None:
    """Main CLI entrypoint supporting both command-line arguments and interactive mode."""
    parser = argparse.ArgumentParser(
        description="Task Manager CLI - Manage tasks and projects using composition"
    )
    parser.add_argument(
        "--file",
        dest="storage_file",
        default=DEFAULT_STORAGE_FILE,
        help="Path to tasks JSON file (default: tasks.json)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'add' command
    add_parser = subparsers.add_parser("add", help="Create and add a new task")
    add_parser.add_argument("title", type=str, help="Task title")
    add_parser.add_argument("-d", "--description", type=str, default="", help="Task description")
    add_parser.add_argument("-s", "--status", type=str, default="Pending", help="Task status (default: Pending)")

    # 'list' command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("-s", "--status", type=str, default=None, help="Filter by status")

    # 'complete' command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("title", type=str, help="Task title to complete")

    # 'remove' command
    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("title", type=str, help="Task title to remove")

    # 'interactive' command
    subparsers.add_parser("interactive", help="Start interactive CLI menu")

    args = parser.parse_args()
    project = load_project(args.storage_file)

    if args.command == "add":
        cmd_add(project, args.title, args.description, args.status, args.storage_file)
    elif args.command == "list":
        cmd_list(project, args.status)
    elif args.command == "complete":
        cmd_complete(project, args.title, args.storage_file)
    elif args.command == "remove":
        cmd_remove(project, args.title, args.storage_file)
    elif args.command == "interactive" or args.command is None:
        if args.command is None and len(sys.argv) > 1:
            parser.print_help()
        else:
            interactive_menu(project, args.storage_file)


if __name__ == "__main__":
    main()
