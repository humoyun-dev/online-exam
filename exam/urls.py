from django.urls import path
from .views import *

urlpatterns = [
    path('', exam_list, name='exam_list'),
    path('add/', add_exam, name='add_exam'),
    path('<int:exam_id>/', exam_detail, name='exam_detail'),
    path('<int:exam_id>/take/', take_exam, name='take_exam'),
    path('<int:exam_id>/delete/', delete_exam, name='delete_exam'),
    path('<int:exam_id>/results/', show_result, name='show_result'),
    path('<int:exam_id>/add_question/', add_question, name='add_question'),
    path('questions/<int:question_id>/', question_detail, name='question_detail'),
    path('questions/<int:question_id>/edit/', edit_question, name='edit_question'),
    path('questions/<int:question_id>/delete/', delete_question, name='delete_question'),
]
