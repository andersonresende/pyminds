from django.shortcuts import render, redirect
from .forms import QuestionForm
from .models import Question


def application_home(request):

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question_form.save()
            return redirect('/')

    question_form = QuestionForm().as_p()
    questions = Question.objects.all()
    return render(request, 'home.html', {'form': question_form, 'questions': questions},)







