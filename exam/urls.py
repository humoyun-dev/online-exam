from django.urls import path
from .views import *

urlpatterns = [
    # path('exam/<int:exam_id>/', exam_detail, name='exam_detail'),
    # path('question/<int:question_id>/', question_detail, name='question_detail'),
    # path('results/', view_results, name='view_results'),

    path('', exam_list, name='exam_list'),
    path('<int:exam_id>/take/', take_exam, name='take_exam'),
    path('<int:exam_id>/result/', show_result, name='show_result'),
]
