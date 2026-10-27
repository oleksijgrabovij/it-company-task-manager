from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from task_manager.models import Task, Worker, TaskType, Position


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "is_completed", "task_type", "assignees"]
        widgets = {'deadline': forms.DateInput(attrs={'type': 'date'})}


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = ('username', 'email', 'first_name', 'last_name', 'position')


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Search by task name...', 'autocomplete': 'off'})
    )

    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        required=False,
        empty_label='All task types',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class WorkerSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=255,
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'placeholder': 'Search by username, first or last name...', 'autocomplete': 'off'}
        )
    )

    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        empty_label='All positions',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class WorkerUpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Worker
        fields = ["username", "first_name", "last_name", "email", "position"]
