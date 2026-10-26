from django import forms
from django.contrib.auth.forms import UserCreationForm
from task_manager.models import Task, Worker, TaskType, Position


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
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
        widget=forms.TextInput(attrs={'placeholder': 'Пошук за назвою...'})
    )

    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        required=False,
        empty_label='Усі типи',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class WorkerSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=255,
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'placeholder': 'Пошук...', 'autocomplete': 'off'}
        )
    )

    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        empty_label='Усі посади',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
