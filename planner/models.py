from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    
    # Canvas assignment tracking
    canvas_id = models.CharField(max_length=100, blank=True, null=True, unique=False)
    external_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
