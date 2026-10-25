from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from task_manager.models import Position, TaskType, Worker, Task

admin.site.register(Position)
admin.site.register(TaskType)
admin.site.register(Worker, UserAdmin)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "deadline", "is_completed", "priority"]
