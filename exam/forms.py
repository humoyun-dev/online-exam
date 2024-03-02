from django import forms
from .models import Option

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
