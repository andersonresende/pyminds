from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('date', 'review', 'forgot')
        widgets = {'text': forms.Textarea(attrs={"placeholder": "Insert your question here..."})}

    tags = forms.CharField(max_length=100, label='', required=False,)
