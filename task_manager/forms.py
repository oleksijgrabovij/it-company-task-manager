from django import forms
from task_manager.models import Task, Worker
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