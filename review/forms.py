from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('date','review')
        widgets = {'text': forms.Textarea(attrs={"placeholder": "Insert your question here..."})}



