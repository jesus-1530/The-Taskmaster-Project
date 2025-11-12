from django.contrib import admin
from django.urls import path
from .views.home import Index, store
from .views.signup import Signup
from .views.login import Login, logout
from .views.orders import OrderView
from .middlewares.auth import auth_middleware


urlpatterns = [
    path('', store, name='goal'),
    path('store/', store, name='store'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('my-stuff/', auth_middleware(OrderView.as_view()), name='my-stuff'),
]