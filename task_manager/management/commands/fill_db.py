from typing import Any
from django.core.management.base import BaseCommand
from task_manager.models import Position, TaskType, Worker, Task


class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args: Any, **kwargs: Any) -> None:
        # 1. Створення посад
        positions = ['Developer', 'Project Manager', 'QA', 'Designer', 'DevOps']
        pos_objs = []
        for p in positions:
            obj, _ = Position.objects.get_or_create(name=p)
            pos_objs.append(obj)

        # 2. Створення типів завдань
        task_types = ['Bug', 'Feature', 'Refactoring', 'Testing', 'Docs']
        tt_objs = []
        for tt in task_types:
            obj, _ = TaskType.objects.get_or_create(name=tt)
            tt_objs.append(obj)

        # 3. Створення працівників
        workers = [
            ('john_dev', 'John', 'Doe', pos_objs[0]),
            ('anna_pm', 'Anna', 'Smith', pos_objs[1]),
            ('mike_qa', 'Mike', 'Johnson', pos_objs[2]),
            ('sara_des', 'Sara', 'Williams', pos_objs[3]),
            ('alex_ops', 'Alex', 'Brown', pos_objs[4]),
        ]
        w_objs = []
        for username, first, last, pos in workers:
            worker, created = Worker.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'position': pos
                }
            )
            if created:
                # Встановлюємо однаковий пароль для всіх тестових юзерів
                worker.set_password('password123')
                worker.save()
            w_objs.append(worker)

        # 4. Створення завдань
        tasks = [
            ('Fix login page', 'Users cant log in.', tt_objs[0], 'High', '2026-12-01'),
            ('Build dashboard', 'Main analytic view.', tt_objs[1], 'Urgent', '2026-12-10'),
            ('Clean up models', 'Refactor DB.', tt_objs[2], 'Medium', '2026-11-20'),
            ('Test payment', 'Check Stripe.', tt_objs[3], 'High', '2026-11-25'),
            ('Write API docs', 'Swagger integration.', tt_objs[4], 'Low', '2026-12-31'),
        ]
        for i, (name, desc, t_type, prio, dline) in enumerate(tasks):
            task, _ = Task.objects.get_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'task_type': t_type,
                    'priority': prio,
                    'deadline': dline
                }
            )
            # Призначаємо по два виконавці на кожне завдання
            task.assignees.add(w_objs[i])
            task.assignees.add(w_objs[(i + 1) % 5])

        self.stdout.write(
            self.style.SUCCESS('Database successfully populated!')
        )
