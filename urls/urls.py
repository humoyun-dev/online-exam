from django.urls import path
from user.views import *
from exam.views import *

urlpatterns = [
    path('students/', student_list, name='student-list'),
    path('students/<int:pk>/', student_detail_view, name='student_detail'),
    path('student/result/', student_results, name='student_results'),
    path('student/result/<int:result_id>/', result_detail, name='result_detail'),
    path('courses/', show_courses, name='show_courses'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('results/', all_results, name="all_results")
]