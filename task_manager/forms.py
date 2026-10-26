from django import forms
from task_manager.models import Task, Worker, TaskType, Position
from django.contrib.auth.forms import UserCreationForm

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {"deadline": forms.DateInput(attrs={"type": "date"})}


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = ("username", "email", "first_name", "last_name", "position")


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Пошук за назвою...",
            "autocomplete": "off",
        }),
    )

    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        required=False,
        empty_label="Усі типи",
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Пошук за username...",
            "autocomplete": "off",
        }),
    )

    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        empty_label="Усі посади",
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )