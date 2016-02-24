from django import forms
from .models import Question, Tag


def create_tags(question, tags):
    if tags and question:
        lst_tags = [Tag.objects.get_or_create(name=t.lower())[0] for t in tags.split(',')]
        [t.questions.add(question) for t in lst_tags]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('date', 'review', 'forgot')
        widgets = {'text': forms.Textarea(attrs={"placeholder": "Insert your question here..."})}

    tags = forms.CharField(max_length=100, label='', required=False,)

    def save(self, force_insert=False, force_update=False, commit=True):
        question = super(QuestionForm, self).save(commit=True)
        tags = self['tags'].value()
        create_tags(question, tags)
        return question

