from django import forms
from .models import Option, Exam


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