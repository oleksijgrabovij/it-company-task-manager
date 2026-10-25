from django.urls import path
from task_manager.views import index, TaskListView, TaskDetailView, PositionListView, TaskTypeListView, WorkerListView

app_name = "task_manager"

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk/", TaskDetailView.as_view(), name="task-detail"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("task-types/", TaskTypeListView.as_view(), name="tasktype-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
]