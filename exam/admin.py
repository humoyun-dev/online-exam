from django.contrib import admin
from .models import Course, Exam, Question, Option, Result

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0

class OptionInline(admin.TabularInline):
    model = Option
    extra = 0

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'course', 'total_marks', 'total_question_number')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'exam', 'content')
    inlines = [OptionInline]

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('option_text', 'question', 'is_correct')

admin.site.register(Course)

# class ResultAdmin(admin.ModelAdmin):
#     list_display = ('student', 'exam', 'mark', 'date_taken', 'display_answers')

#     def display_answers(self, obj):
#         # Custom method to display answers in admin
#         if obj.answers:
#             return ', '.join(f"Question ID: {question_id}, Selected Option ID: {answer.get('selected_option_id', '-')}, Correct: {answer.get('is_correct', False)}" for question_id, answer in obj.answers.items())
#         else:
#             return '-'
#     display_answers.short_description = 'Answers'

admin.site.register(Result)