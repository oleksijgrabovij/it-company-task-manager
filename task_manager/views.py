from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import (
    TaskForm,
    TaskSearchForm,
    WorkerCreationForm,
    WorkerSearchForm,
    WorkerUpdateForm,
)
from task_manager.models import Position, Task, TaskType, Worker


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self: "StaffRequiredMixin") -> bool:
        return self.request.user.is_staff


@login_required
def index(request: HttpRequest) -> HttpResponse:
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
    return render(request, "task_manager/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5
    ordering = ["name"]

    def get_context_data(
        self: "TaskListView",
        *,
        object_list: Any = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        context = super().get_context_data(object_list=object_list, **kwargs)
        name = self.request.GET.get("name", "")
        task_type = self.request.GET.get("task_type", "")

        context["search_form"] = TaskSearchForm(
            initial={"name": name, "task_type": task_type}
        )
        return context

    def get_queryset(self: "TaskListView") -> QuerySet[Any]:
        queryset = super().get_queryset().select_related("task_type")
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data.get("name"):
                queryset = queryset.filter(
                    name__icontains=form.cleaned_data["name"]
                )
            if form.cleaned_data.get("task_type"):
                queryset = queryset.filter(
                    task_type=form.cleaned_data["task_type"]
                )

        return queryset


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5
    ordering = ["username"]

    def get_context_data(
        self: "WorkerListView",
        *,
        object_list: Any = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        context = super().get_context_data(object_list=object_list, **kwargs)
        search_query = self.request.GET.get("search_query", "")
        position = self.request.GET.get("position", "")

        context["search_form"] = WorkerSearchForm(
            initial={"search_query": search_query, "position": position}
        )
        return context

    def get_queryset(self: "WorkerListView") -> QuerySet[Any]:
        queryset = super().get_queryset().select_related("position")
        form = WorkerSearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data.get("search_query"):
                query = form.cleaned_data["search_query"]
                q_objects = Q(username__icontains=query)
                q_objects |= Q(first_name__icontains=query)
                q_objects |= Q(last_name__icontains=query)
                queryset = queryset.filter(q_objects)
            if form.cleaned_data.get("position"):
                queryset = queryset.filter(
                    position=form.cleaned_data["position"]
                )

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(
    LoginRequiredMixin, StaffRequiredMixin, generic.DeleteView
):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5
    ordering = ["name"]


class PositionCreateView(
    LoginRequiredMixin, StaffRequiredMixin, generic.CreateView
):
    model = Position
    fields = ["name"]
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdateView(
    LoginRequiredMixin, StaffRequiredMixin, generic.UpdateView
):
    model = Position
    fields = ["name"]
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(
    LoginRequiredMixin, StaffRequiredMixin, generic.DeleteView
):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5
    ordering = ["name"]


class TaskTypeCreateView(
    LoginRequiredMixin, StaffRequiredMixin, generic.CreateView
):
    model = TaskType
    fields = ["name"]
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdateView(
    LoginRequiredMixin, StaffRequiredMixin, generic.UpdateView
):
    model = TaskType
    fields = ["name"]
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(
    LoginRequiredMixin, StaffRequiredMixin, generic.DeleteView
):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-type-list")
