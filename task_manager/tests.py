from django.test import TestCase
from task_manager.models import Position, TaskType, Worker, Task


class PositionModelTest(TestCase):
    def test_position_str(self: 'PositionModelTest') -> None:
        position = Position.objects.create(name='Developer')
        self.assertEqual(str(position), 'Developer')


class TaskTypeModelTest(TestCase):
    def test_task_type_str(self: 'TaskTypeModelTest') -> None:
        task_type = TaskType.objects.create(name='Bug')
        self.assertEqual(str(task_type), 'Bug')


class WorkerModelTest(TestCase):
    def test_worker_str(self: 'WorkerModelTest') -> None:
        worker = Worker.objects.create(
            username='testuser',
            first_name='Ivan',
            last_name='Ivanov',
            password='testpassword123'
        )
        self.assertEqual(str(worker), 'testuser')


class TaskModelTest(TestCase):
    def test_task_str(self: 'TaskModelTest') -> None:
        task_type = TaskType.objects.create(name='New feature')
        task = Task.objects.create(
            name='Test task',
            description='Task description',
            deadline='2026-12-31',
            task_type=task_type
        )
        self.assertEqual(str(task), 'Test task')
