from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from task_manager.models import Position, Task, TaskType

Worker = get_user_model()


class PositionModelTest(TestCase):
    def test_position_str(self: "PositionModelTest") -> None:
        position = Position.objects.create(name="Developer")
        self.assertEqual(str(position), "Developer")


class TaskTypeModelTest(TestCase):
    def test_task_type_str(self: "TaskTypeModelTest") -> None:
        task_type = TaskType.objects.create(name="Bug")
        self.assertEqual(str(task_type), "Bug")


class WorkerModelTest(TestCase):
    def test_worker_str(self: "WorkerModelTest") -> None:
        worker = Worker.objects.create(
            username="testuser",
            first_name="Ivan",
            last_name="Ivanov",
            password="testpassword123",
        )
        self.assertEqual(str(worker), "testuser")


class TaskModelTest(TestCase):
    def test_task_str(self: "TaskModelTest") -> None:
        task_type = TaskType.objects.create(name="New feature")
        task = Task.objects.create(
            name="Test task",
            description="Task description",
            deadline="2026-12-31",
            task_type=task_type,
        )
        self.assertEqual(str(task), "Test task")


class PublicViewTests(TestCase):
    def test_login_required_for_tasks(self: "PublicViewTests") -> None:
        """Test that task list view requires login."""
        res = self.client.get(reverse("task_manager:task-list"))
        self.assertNotEqual(res.status_code, 200)
        self.assertTrue(res.url.startswith(reverse("login")))


class PrivateViewTests(TestCase):
    def setUp(self: "PrivateViewTests") -> None:
        self.user = Worker.objects.create_user(
            username="tester", password="testpassword123"
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Test Task",
            description="Test description",
            deadline="2026-12-31",
            task_type=self.task_type,
        )

    def test_retrieve_tasks_list(self: "PrivateViewTests") -> None:
        """Test retrieving list of tasks."""
        res = self.client.get(reverse("task_manager:task-list"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.task.name)

    def test_task_search_works(self: "PrivateViewTests") -> None:
        """Test that search by name works correctly."""
        res = self.client.get(
            reverse("task_manager:task-list") + "?name=Test"
        )
        self.assertContains(res, self.task.name)
