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
        for n in range(1,11):
            response = client.post('/', data={'text': 'q%s' % n})
        questions = Question.objects.all()
        self.assertEqual(10, len(questions))
        reviews = Review.objects.all()
        self.assertEqual(1, len(reviews))
        schedules = Schedule.objects.all()
        self.assertEqual(5, len(schedules))
        for q in questions:
            self.assertEqual(reviews[0], q.review)
        for s in schedules:
            self.assertEqual(reviews[0], s.review)




