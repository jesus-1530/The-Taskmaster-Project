from django.apps import AppConfig


class TodolistConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "todolist"

    def ready(self):
        from django.contrib.auth.models import User
        from django.db.models.signals import post_save
        from .models import UserProfile

        def create_profile(sender, instance, created, **kwargs):
            if created:
                UserProfile.objects.create(user=instance)
        post_save.connect(create_profile, sender=User)
