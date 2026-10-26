from typing import Any
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task, Worker, Position, TaskType
from .forms import (
    TaskForm,
    WorkerCreationForm,
    TaskSearchForm,
    WorkerSearchForm
)


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()
    num_positions = Position.objects.count()
    num_task_types = TaskType.objects.count()

    context = {
        'num_tasks': num_tasks,
        'num_workers': num_workers,
        'num_positions': num_positions,
        'num_task_types': num_task_types,
    }
    return render(request, 'task_manager/index.html', context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(
        self: 'TaskListView',
        *,
        object_list: Any = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        context = super().get_context_data(object_list=object_list, **kwargs)
        name = self.request.GET.get('name', '')
        task_type = self.request.GET.get('task_type', '')

        context['search_form'] = TaskSearchForm(
            initial={'name': name, 'task_type': task_type}
        )
        return context

    def get_queryset(self: 'TaskListView') -> QuerySet[Any]:
        queryset = super().get_queryset()
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data.get('name'):
                queryset = queryset.filter(
                    name__icontains=form.cleaned_data['name']
                )
            if form.cleaned_data.get('task_type'):
                queryset = queryset.filter(
                    task_type=form.cleaned_data['task_type']
                )

        return queryset


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(
        self: 'WorkerListView',
        *,
        object_list: Any = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        context = super().get_context_data(object_list=object_list, **kwargs)
        search_query = self.request.GET.get('search_query', '')
        position = self.request.GET.get('position', '')

        context['search_form'] = WorkerSearchForm(
            initial={'search_query': search_query, 'position': position}
        )
        return context

    def get_queryset(self: 'WorkerListView') -> QuerySet[Any]:
        queryset = super().get_queryset()
        form = WorkerSearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data.get('search_query'):
                queryset = queryset.filter(
                    username__icontains=form.cleaned_data['search_query']
                )
            if form.cleaned_data.get('position'):
                queryset = queryset.filter(
                    position=form.cleaned_data['position']
                )

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task_manager:task-list')


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task_manager:task-list')


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('task_manager:task-list')


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy('task_manager:worker-list')


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy('task_manager:worker-list')


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy('task_manager:worker-list')


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = '__all__'
    success_url = reverse_lazy('task_manager:position-list')


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = '__all__'
    success_url = reverse_lazy('task_manager:position-list')


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy('task_manager:position-list')


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = '__all__'
    success_url = reverse_lazy('task_manager:task-type-list')


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = '__all__'
    success_url = reverse_lazy('task_manager:task-type-list')


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy('task_manager:task-type-list')
