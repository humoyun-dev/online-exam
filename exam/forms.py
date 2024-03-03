from django import forms
from .models import *
from django.forms import inlineformset_factory


class OptionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(OptionForm, self).__init__(*args, **kwargs)
        for question in questions:
            options = Option.objects.filter(question=question)
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=[(option.id, option.option_text) for option in options],
                widget=forms.RadioSelect,
                label=question.question_text
            )

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['course', 'exam_name', 'total_marks', 'total_question_number']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'content', 'mark']

OptionFormSet = forms.inlineformset_factory(
    Question, Option, fields=('option_text', 'is_correct'), extra=4, can_delete=False
)