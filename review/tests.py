# -*- coding:utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import datetime
from django.test import TestCase, Client
from .models import Question, Review, Schedule, Tag
from .views import *


def r_test(lst_items, method, fix_value, alt_value):
    if not len(lst_items):
        return
    value = getattr(lst_items[0], alt_value)
    method(fix_value, value)
    r_test(lst_items[1:], method, value, alt_value)

c_schedule = lambda x: Schedule.objects.create(**x)
calc_date_before = lambda x: datetime.date.today() - datetime.timedelta(x)
calc_date_after = lambda x: datetime.date.today() + datetime.timedelta(x)

class FunctionsTest(TestCase):

    def test_function_create_review(self):
        questions = [Question.objects.create(text='q%s' % n) for n in range(1, 11)]
        review = create_review(questions)
        reviews = Review.objects.all()
        self.assertEqual(1, len(reviews))
        self.assertEqual(review, reviews[0])
        questions = Question.objects.all()
        for q in questions:
            self.assertEqual(q.review, review)

    def test_function_create_schedules(self):
        review = Review.objects.create()
        create_schedules(review, 5, 10)
        schedules = Schedule.objects.all()
        self.assertEqual(2, len(schedules))
        for s in schedules:
            self.assertEqual(s.review, review)

class MainTest(TestCase):

    def test_home(self):
        """
        Testa se ao chamar a url '/' a home e retornada.

        """
        client = Client()
        response = client.get('/')
        self.assertTemplateUsed(response,'home.html')

    def test_home_post_save_questions_and_redirects_correct(self):
        """
        Testa se as questions estao sendo salvas na home e
        esta sendo redirecionado corretamente alterando a quantidade
        de questoes.

        """
        client = Client()
        response = client.get('/')
        count_questions = len(Question.objects.all()) + 1
        self.assertContains(response, 'Question %s' % count_questions)
        response = client.post('/', data={'text': 'question one'})
        questions = Question.objects.all()
        self.assertEqual(1, len(questions))
        self.assertEqual('question one', questions[0].text)
        self.assertRedirects(response, '/')
        response = client.get('/')
        count_questions = len(Question.objects.all()) + 1
        self.assertContains(response, 'Question %s' % count_questions)

    def test_home_post_save_question_without_text_and_return_template(self):
        """
        Testa se ao tentar salvar uma question sem texto e
        redirecionado de volta a home e nenhuma questao e salva.

        """
        client = Client()
        response = client.post('/',data={'text': ''})
        questions = Question.objects.all()
        self.assertEqual(0, len(questions))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_post_save_ten_questions_create_review_and_schedules(self):
        """
        Testa se ao criar 10 questions uma review e criada e tambem
        cinco schedules, vinculados a review.

        """
        client = Client()
        for n in range(1,6):
            response = client.post('/', data={'text': 'q%s' % n})
        questions = Question.objects.all()
        self.assertEqual(5, len(questions))
        reviews = Review.objects.all()
        self.assertEqual(1, len(reviews))
        schedules = Schedule.objects.all()
        self.assertEqual(5, len(schedules))
        for q in questions:
            self.assertEqual(reviews[0], q.review)
        for s in schedules:
            self.assertEqual(reviews[0], s.review)

    def test_home_return_schedules_on_date(self):
        """
        Testa se a home retorna as schedules corretas de acordo com suas
        datas.
        """
        review = Review()
        review.save()
        today = datetime.date.today()
        before_today = today - datetime.timedelta(10)
        after_today = today + datetime.timedelta(10)
        for d in [today, before_today, after_today]:
            s = Schedule()
            s.date = d
            s.review = review
            s.save()

        schedules = Schedule.objects.all()
        self.assertEqual(3, len(schedules))
        client = Client()
        response = client.get('/')
        self.assertContains(response, 'Schedules: '+str(len(schedules)))
        self.assertContains(response, 'Schedule '+str(schedules[0].date))
        self.assertContains(response, 'Schedule '+str(schedules[1].date))
        self.assertNotContains(response, 'Schedule '+str(schedules[2].date))

    def test_home_return_schedules_on_next_date(self):
        """
        Testa se a home retorna proxima schedule de acordo com suas
        datas.
        """
        review = Review()
        review.save()

        lst_dates = [[0, 10, 10, 15, 25], [0, 5, 5, 9, 10]]
        for lst in lst_dates:
            lst_schedules = [c_schedule({'date': d, 'review': review}) for d in map(calc_date_after, lst)]
            client = Client()
            response = client.get('/')
            self.assertContains(response, 'next %s' % lst_schedules[1].date.strftime('%d/%m/%Y'))


    def test_schedule_page(self):
        """
        Testa se a pagina de schedule e chamada corretamente, retornando
        a review e as questoes relacionadas.
        """
        questions = [Question.objects.create(text='q%s' % n) for n in range(1, 11)]
        review = create_review(questions)

        schedule = Schedule()
        schedule.date = datetime.date.today()
        schedule.review = review
        schedule.save()

        client = Client()
        response = client.get('/schedule/%s/'% schedule.id)
        self.assertTemplateUsed(response, 'schedule.html')
        self.assertContains(response, 'Schedule '+str(schedule.date))
        self.assertContains(response, 'Review '+str(review.pk))

        def recursive(questions):
            if len(questions) == 0:
                return True
            self.assertContains(response, questions[0].text)
            return recursive(questions[1:])

        recursive(questions)

    def test_schedule_page_post_checked(self):
        """
        Testa se a checarmos uma schedule, somos redirecionados a home
        e a schedule nao aparece mais.
        """
        questions = [Question.objects.create(text='q%s' % n) for n in range(1, 11)]
        review = create_review(questions)

        schedule = Schedule()
        schedule.date = datetime.date.today()
        schedule.review = review
        schedule.save()

        client = Client()
        response = client.get('/')
        self.assertContains(response, 'Schedule '+str(schedule.date))

        self.assertFalse(schedule.checked)
        response = client.post('/schedule/%s/'% schedule.id)
        schedule = Schedule.objects.get(id=schedule.id)
        self.assertTrue(schedule.checked)

        self.assertRedirects(response, '/')
        response = client.get('/')
        self.assertNotContains(response, 'Schedule '+str(schedule.date))


    def test_tags_model_creation_with_questions(self):
        """Testa a criacao de uma tag e a sua ligacao com questions."""
        r = Review.objects.create()
        list_questions = [Question.objects.create(text="Q%s" % n) for n in range(2)]

        tag = Tag.objects.create(name="tag1")
        [tag.questions.add(q) for q in list_questions]

        tags_list = Tag.objects.all()
        self.assertEqual(1, len(tags_list))
        
        list_questions = tag.questions.all()
        self.assertEqual(2, len(list_questions))
        [self.assertEqual(tag.pk, q.tag_set.all()[0].pk) for q in list_questions]

    def test_home_post_save_question_and_tag(self):
        client = Client()
        tags = ['tg1', 'tg2']
        response = client.post("/", data={'text': 'Question1', 'tags': ','.join(tags)})
        self.assertRedirects(response, '/')
        lst_questions = Question.objects.all()
        self.assertEqual(1, len(lst_questions))
        lst_tags = Tag.objects.all()
        self.assertEqual(2, len(lst_tags))

    def test_home_post_save_question_and_tags_autocomplete_and_not_duplicate(self):
        client = Client()
        tags = ['tg1', 'tg2']
        for x in range(2):
            response = client.post("/", data={'text': 'Question1', 'tags': ','.join(tags)})
        response = client.get("/")
        [self.assertContains(response, t) for t in tags]
        self.assertEqual(2, Tag.objects.all().count())

    def test_post_save_tags_lowercase(self):
        client = Client()
        tags = ['TG1', 'tg2']
        response = client.post("/", data={'text': 'Question1', 'tags': ','.join(tags)})
        lst_tags = Tag.objects.all()
        [self.assertEqual(t.name, t.name.lower()) for t in lst_tags]

    def test_get_schedule_page_show_questions_and_tags(self):
        questions = [Question.objects.create(text='q%s' % n) for n in range(1, 6)]
        lst_tags = ['tg1','tg2']
        lst_tags = [Tag.objects.create(name=t) for t in lst_tags]
        tag1, tag2 = lst_tags
        [tag1.questions.add(q) for q in questions[:2]]
        [tag2.questions.add(q) for q in questions[2:]]
        create_all()
        schedules = Schedule.objects.all()
        client = Client()
        response = client.get('/schedule/%s/'% schedules[0].id)
        self.assertTemplateUsed(response, 'schedule.html')
        self.assertContains(response, 'Schedule '+str(schedules[0].date))
        self.assertContains(response, tag1.name)
        self.assertContains(response, tag2.name)

    def test_home_schedules_ordered(self):
        review = Review()
        review.save()
        lst_schedules_older = [c_schedule({'date': d, 'review': review}) for d in map(calc_date_before, [0, 10, 15, 25])]
        lst_schedules = Schedule.get_current_shedules()
        cont = 3
        for sh in lst_schedules:
            self.assertEqual(sh.date, lst_schedules_older[cont].date)
            cont -= 1


# Map não é possivel chamar funções passando os argumentos diretamente.
# Map não é possivel passar mais de um argumento na função.
# no entanto se vc for usar funcoes, precisando apenas de um map e um compression,
# o map tem uma sintaxe mais interessante.



