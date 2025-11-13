from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    task = models.CharField(max_length=200)
    task_desc = models.CharField(max_length=500, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    point_value = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    canvas_token = models.CharField(max_length=255, blank=True, null=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} Profile"
