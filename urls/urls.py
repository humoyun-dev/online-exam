from django.urls import path
from user.views import *

urlpatterns = [
    path('students/', student_list, name='student-list'),
    path('students/<int:pk>/', student_detail_view, name='student_detail'),
]