import json

from random import shuffle

from django.views.generic import FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import View
from django.http import HttpResponse

from review.forms import QuestionForm
from review.models import Question, Schedule, Tag
from review.helpers import create_tags, create_all


class HomeView(FormView):
    success_url = reverse_lazy('review:home')
    template_name = 'home.html'
    form_class = QuestionForm

    def form_valid(self, form):
        question = form.save()
        tags = form['tags'].value()
        if tags:
            create_tags(question, tags)
        create_all()
        response = super(HomeView, self).form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['schedules'] = Schedule.objects.currents()
        context['next_schedule'] = Schedule.get_next_schedule()
        context['count_schedules'] = Schedule.objects.filter(
            checked=False
        ).count()
        context['number_next_question'] = Question.objects.all().count() + 1
        tags_name = [str(t['name']) for t in Tag.objects.all().values('name')]
        context['tags'] = ','.join(tags_name)
        return context


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
        questions = questions.filter(tags__in=tags)
    if quant:
        quant = int(quant)
        questions = list(questions[:quant])
        shuffle(questions)
    return render(request, 'questions.html', {'questions': questions})


def closed_questions(request):
    questions_list = Question.objects.closeds().order_by('?')[:10]
    return render(request, 'questions.html', {'questions': questions_list})


class ForgotQuestionView(View):

    def post(self, request, *args, **kwargs):
        question_pk = request.POST.get('pk')
        question = get_object_or_404(Question, pk=question_pk)
        question.update_forgot()
        return HttpResponse(
            json.dumps({'message': 'Success updated'}),
            content_type="application/json")
