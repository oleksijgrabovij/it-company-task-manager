from django.shortcuts import render
from task_manager.models import Task, TaskType, Position, Worker

def index(request):
    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()
    num_positions = Position.objects.count()
    num_task_types = TaskType.objects.count()
    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
        "num_positions": num_positions,
        "num_task_types": num_task_types,
    }
    return render(request, 'task_manager/index.html', context=context)
