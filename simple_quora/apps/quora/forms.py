from django import forms
from django.core.exceptions import ValidationError

from apps.quora.models import Question, Answer

class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['body']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('body'):
            raise ValidationError("Question cannot be blank")
        return cleaned_data

class AnswerForm(forms.ModelForm):
    
    class Meta:
        model = Answer
        fields = ['body']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('body'):
            raise ValidationError("Answer cannot be blank")
        return cleaned_data

    