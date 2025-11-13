from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('sync_canvas/', views.sync_canvas, name='sync_canvas'),
    path('save_token/', views.save_token, name='save_token'),
    path('tasks-json/', views.tasks_json, name='tasks_json'),
    path('', views.shop, name='shop'),
]
