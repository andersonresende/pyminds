from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from rest_framework import status

from review.models import Question


class CreateQuestionTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('review-endpoints:create-question')
        self.params = {'text': 'test question'}
        self.params_with_tags = {
            'text': 'test question',
            'tags': 'tag1, tag2',
        }

    def test_create_question_success(self):
        response = self.client.post(self.url, self.params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_question_with_invalid_params(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_question_and_tags(self):
        self.client.post(self.url, self.params_with_tags)
        question = Question.objects.first()
        tags = question.tags.all()
        self.assertEqual(question.text, self.params_with_tags['text'])
        self.assertEqual(len(tags), 2)

    def test_create_question_and_review(self):
        pass
