from django.urls import path
from task_manager.views import index, TaskListView, TaskDetailView

app_name = "task_manager"

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="tasks"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
]