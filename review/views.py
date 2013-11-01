import datetime
from django.shortcuts import render, redirect, get_object_or_404
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
            if len(questions) == 5:
                review = create_review(questions)
                create_schedules(review, 5, 10, 20, 30, 40)
            return redirect('/')
    question_form = QuestionForm().as_p()
    schedules = Schedule.get_current_shedules()

    next_schedule = Schedule.get_next_schedule()

    count_schedules = len(Schedule.objects.filter(checked=False))
    number_next_question = len(Question.objects.all()) + 1
    return render(request, 'home.html', {
        'form': question_form,
        'schedules': schedules,
        'count_schedules': count_schedules,
        'next_schedule': next_schedule,
        'number_next_question': number_next_question
    },)


def schedule_page(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    if request.method == 'POST':
        schedule.checked = True
        schedule.save()
        return redirect('/')

    return render(request, 'schedule.html', {'schedule':schedule,})







