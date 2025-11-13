from django.contrib import admin
from .models import UserProfile, Task

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "points", "canvas_token")
    search_fields = ("user__username",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("task", "user", "due_date", "point_value", "completed")
    list_filter = ("completed", "user")
    search_fields = ("task", "task_desc")
