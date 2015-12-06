import datetime
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.http import HttpResponse

from .forms import QuestionForm
from .models import Question, Review, Schedule, Tag


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


def create_all():
    questions = Question.objects.filter(review=None)
    if questions.count() == 5:
        review = create_review(questions)
        create_schedules(review, 5, 15, 35, 60, 90)

#talvez todos esses metodos acima deveriam estar no save de um objeto review

def application_home(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question_form.save()
            create_all()
            return redirect('/')

    question_form = QuestionForm().as_p()
    schedules = Schedule.objects.currents()
    next_schedule = Schedule.get_next_schedule()
    count_schedules = Schedule.objects.filter(checked=False).count()
    number_next_question = Question.objects.all().count() + 1
    tags_name = [str(t['name']) for t in Tag.objects.all().values('name')]
    tags = ','.join(tags_name)
    return render(request, 'home.html', {
        'form': question_form,
        'schedules': schedules,
        'count_schedules': count_schedules,
        'next_schedule': next_schedule,
        'number_next_question': number_next_question,
        'tags': tags,
    },)


def schedule_page(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    if request.method == 'POST':
        review = schedule.review
        Schedule.close_last_schedules(review)
        return redirect('/')

    return render(request, 'schedule.html', {'schedule': schedule})


def questions(request):
    questions = Question.objects.all()
    quant = request.GET.get('quant', None)
    tags = request.GET.get('tags', None)
    if tags:
        tags_name = tags.split(',')
        tags = Tag.objects.filter(name__in=tags_name)
        questions = questions.filter(tag__in=tags)
    if quant:
        quant = int(quant)
        questions = questions[:quant]

    return render(request, 'questions.html', {'questions': questions})


def closed_questions(request):
    questions_list = Question.objects.closeds().order_by('?')[:10]
    return render(request, 'questions.html', {'questions': questions_list})


class ForgotQuestionView(View):

    def post(self, request, *args, **kwargs):
        question_pk = kwargs.get('pk')
        question = get_object_or_404(Question, pk=question_pk)
        question.update_forgot()
        return HttpResponse(
            json.dumps({'message': 'Success updated'}),
            content_type="application/json")
