"""
Unit tests for Task and Project classes.
"""
import unittest
from task import Task
from project import Project


class TestTaskManager(unittest.TestCase):
    def test_task_creation_success(self):
        task = Task(title="Buy groceries", description="Milk, Eggs, Bread", status="Pending")
        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.description, "Milk, Eggs, Bread")
        self.assertEqual(task.status, "Pending")
        self.assertFalse(task.is_completed())

    def test_task_empty_title_raises_error(self):
        with self.assertRaises(ValueError):
            Task(title="")
        with self.assertRaises(ValueError):
            Task(title="   ")

    def test_task_status_updates(self):
        task = Task(title="Write documentation")
        self.assertEqual(task.status, "Pending")
        task.mark_in_progress()
        self.assertEqual(task.status, "In Progress")
        task.mark_completed()
        self.assertEqual(task.status, "Completed")
        self.assertTrue(task.is_completed())

    def test_composition_not_inheritance(self):
        # Verify that Project does NOT inherit from Task
        self.assertFalse(issubclass(Project, Task))
        self.assertFalse(issubclass(Task, Project))

        project = Project(name="Q1 Roadmap")
        self.assertFalse(isinstance(project, Task))

    def test_project_task_composition(self):
        project = Project(name="Task Manager MVP", description="Build initial CLI")
        t1 = Task(title="Design Task class", description="Store title, description, status")
        t2 = Task(title="Design Project class", description="Compose tasks")

        project.add_task(t1)
        project.add_task(t2)

        self.assertEqual(project.total_tasks(), 2)
        self.assertEqual(len(project.tasks), 2)
        self.assertEqual(project.get_task("Design Task class"), t1)
        self.assertEqual(project.get_task("Design Project class"), t2)

    def test_project_duplicate_task_raises_error(self):
        project = Project(name="Demo")
        t1 = Task(title="Setup CI")
        project.add_task(t1)
        with self.assertRaises(ValueError):
            project.add_task(Task(title="Setup CI"))

    def test_project_list_tasks_filtering(self):
        project = Project(name="Sprint 1")
        t1 = Task(title="Task 1", status="Pending")
        t2 = Task(title="Task 2", status="In Progress")
        t3 = Task(title="Task 3", status="Completed")

        project.add_task(t1)
        project.add_task(t2)
        project.add_task(t3)

        self.assertEqual(len(project.list_tasks()), 3)
        self.assertEqual(len(project.list_tasks(status="Pending")), 1)
        self.assertEqual(len(project.list_tasks(status="Completed")), 1)
        self.assertEqual(len(project.list_tasks(status="In Progress")), 1)

    def test_project_remove_task(self):
        project = Project(name="Cleanup")
        t1 = Task(title="Old task")
        project.add_task(t1)
        self.assertTrue(project.remove_task("Old task"))
        self.assertEqual(project.total_tasks(), 0)
        self.assertFalse(project.remove_task("Nonexistent task"))

    def test_serialization_roundtrip(self):
        project = Project(name="Backend Service", description="Core API")
        t1 = Task(title="Auth Endpoint", description="JWT login", status="Completed")
        project.add_task(t1)

        project_dict = project.to_dict()
        reconstructed = Project.from_dict(project_dict)

        self.assertEqual(reconstructed.name, "Backend Service")
        self.assertEqual(reconstructed.description, "Core API")
        self.assertEqual(reconstructed.total_tasks(), 1)
        self.assertEqual(reconstructed.tasks[0].title, "Auth Endpoint")
        self.assertEqual(reconstructed.tasks[0].status, "Completed")


if __name__ == "__main__":
    unittest.main()
