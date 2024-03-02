from django.urls import path
from django.contrib.auth import views as auth_views
from .views import custom_login

urlpatterns = [
    path('login/', custom_login, name='login'),
]
