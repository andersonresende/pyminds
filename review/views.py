import datetime
from django.shortcuts import render, redirect
from .forms import QuestionForm
from .models import Question, Review, Schedule


def create_schedules(review, *args):
    today = datetime.datetime.today()
    for d in args:
        schedule = Schedule(date=today+datetime.timedelta(d), review=review)
        schedule.save()


def create_review(questions):
    review = Review()
    review.save()
    for q in questions:
        q.review = review
        q.save()
    return review


def application_home(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question_form.save()
            questions = Question.objects.filter(review=None)
            if len(questions) == 10:
                review = create_review(questions)
                create_schedules(review, 5, 10, 20, 30, 40)
            return redirect('/')
    question_form = QuestionForm().as_p()
    reviews = Review.objects.all()
    return render(request, 'home.html', {'form': question_form, 'reviews': reviews},)







