from django.contrib import admin
from .models import *

class OptionInline(admin.TabularInline):
    model = Option
    extra = 3

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'course', 'total_marks', 'total_question_number')
    inlines = [QuestionInline]

    def get_formsets_with_inlines(self, request, obj=None):
        # Override the method to include both Question and Option inlines for existing and new exams
        formsets_with_inlines = super().get_formsets_with_inlines(request, obj)

        for formset, inline in formsets_with_inlines:
            if not hasattr(inline, 'model'):
                # If the inline doesn't have a model attribute, it means it's a tuple with only two values
                formset, inline = inline, None
            yield formset, inline

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'content', 'mark')
    inlines = [OptionInline]

admin.site.register(Course)
admin.site.register(Result)