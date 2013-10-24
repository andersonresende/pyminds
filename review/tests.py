"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import datetime
from django.test import TestCase, Client
from .models import Question, Review, Schedule
from .views import create_review, create_schedules


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
        esta sendo redirecionado corretamente.

        """
        client = Client()
        response = client.post('/',data={'text': 'question one'})
        questions = Question.objects.all()
        self.assertEqual(1, len(questions))
        self.assertEqual('question one', questions[0].text)
        self.assertRedirects(response, '/')

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
        self.assertContains(response, 'Schedule '+str(schedules[0].date))
        self.assertContains(response, 'Schedule '+str(schedules[1].date))
        self.assertNotContains(response, 'Schedule '+str(schedules[2].date))


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


