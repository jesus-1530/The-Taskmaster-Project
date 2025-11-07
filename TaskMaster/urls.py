"""
URL configuration for TaskMaster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from planner.views import task_list
from planner.views import task_list, tasks_json
from store.views.home import Index, store
#from store.views.signup import Signup
##from store.views.login import Login, logout
#from store.views.orders import OrderView
from . import settings
from planner.views import task_list, tasks_json, add_task, delete_task

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store', store, name='store'),
    #path('signup', Signup.as_view, name='signup'),
    #path('login', Login.as_view, name='login'),
    #path('my stuff', OrderView.as_view, name='my stuff'),
    path('store/', include('store.urls')),
    path('', task_list, name='task_list'),
    path('tasks-json/', tasks_json, name='tasks_json'),
    path('add-task/', add_task, name='add_task'),
    path('delete-task/', delete_task, name='delete_task'),
]
