# -*- coding:utf-8 -*-

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from mommy_recipes import review_recipe, question_recipe
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


def c_schedules(calc_date_func, review, dates=None):
    """
    That function creates schedules by review before or after date.
    """
    dates = dates or [0, 10, 15, 25]
    return [c_schedule({'date': d, 'review': review})
            for d in map(calc_date_func, dates)]


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
        review = Review.objects.create()
        today = datetime.date.today()
        before_today = today - datetime.timedelta(10)
        after_today = today + datetime.timedelta(10)
        for d in [today, before_today, after_today]:
            c_schedule({'date': d, 'review': review})
        schedules = Schedule.objects.all()
        client = Client()
        response = client.get('/')
        self.assertContains(response, schedules[1])
        self.assertNotContains(response, schedules[0])
        self.assertNotContains(response, schedules[2])

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
        self.assertContains(response, schedule)
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
        self.assertContains(response, schedule)

        self.assertFalse(schedule.checked)
        response = client.post('/schedule/%s/'% schedule.id)
        schedule = Schedule.objects.get(id=schedule.id)
        self.assertTrue(schedule.checked)

        self.assertRedirects(response, '/')
        response = client.get('/')
        self.assertNotContains(response, schedule)

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
        lst_tags = ['tg1', 'tg2']
        lst_tags = [Tag.objects.create(name=t) for t in lst_tags]
        tag1, tag2 = lst_tags
        [tag1.questions.add(q) for q in questions[:2]]
        [tag2.questions.add(q) for q in questions[2:]]
        create_all()
        schedules = Schedule.objects.all()
        client = Client()
        response = client.get('/schedule/%s/'% schedules[0].id)
        self.assertTemplateUsed(response, 'schedule.html')
        self.assertContains(response, schedules[0])
        self.assertContains(response, tag1.name)
        self.assertContains(response, tag2.name)

    def test_tags_ordered_by_name(self):
        tags_name = ['tg3', 'tg1', 'tg2', 'tg5', 'tg4']
        lst_tags = [Tag.objects.create(name=t) for t in tags_name]
        q_tags = Tag.objects.all()
        self.assertEqual(tags_name[1], q_tags[0].name)
        self.assertEqual(tags_name[2], q_tags[1].name)
        self.assertEqual(tags_name[0], q_tags[2].name)
        self.assertEqual(tags_name[4], q_tags[3].name)
        self.assertEqual(tags_name[3], q_tags[4].name)

    def test_get_questions_quant_and_tag(self):
        questions = [Question.objects.create(text='q%s' % n) for n in range(1, 6)]
        lst_tags = ['tg1', 'tg2']
        lst_tags = [Tag.objects.create(name=t) for t in lst_tags]
        tag1, tag2 = lst_tags
        [tag1.questions.add(q) for q in questions[:2]]
        [tag2.questions.add(q) for q in questions[2:]]

        tags = ','.join([t.name for t in lst_tags])
        quant = ''
        url = '/questions/?tags={0}&quant={1}'.format(tags, quant)

        client = Client()
        response = client.get(url)

        def recursive(questions):
            if questions:
                self.assertContains(response, questions[0].text)
                recursive(questions[1:])

        recursive(questions)

        tags = ','.join([t for t in ['tg1']])
        quant = 3
        url = '/questions/?tags={0}&quant={1}'.format(tags, quant)
        response = client.get(url)

        questions = questions[3:]
        def recursive(questions):
            if questions:
                self.assertNotContains(response, questions[0].text)
                recursive(questions[1:])

        recursive(questions)

    def test_get_just_one_schedule_for_time(self):
        """
        Tests if just one schedule for review is returned when existing
        other schedules open.
        """
        review = Review.objects.create()
        for d in map(calc_date_before, [0, 10, 15, 25]):
            c_schedule({'date': d, 'review': review})
        response = self.client.get('/')
        self.assertEqual(len(response.context['schedules']), 1)

    def test_get_ordered_schedules(self):
        """
        Tests if the schedules are returned ordered by date.
        """
        review_one, review_two, review_tree = review_recipe.make(_quantity=3)
        schedules_one = c_schedules(calc_date_before, review_one, [5])
        schedules_two = c_schedules(calc_date_before, review_two, [6])
        schedules_tree = c_schedules(calc_date_before, review_tree, [7])
        schedules = Schedule.objects.currents()
        self.assertEqual(schedules[0], schedules_one[0])
        self.assertEqual(schedules[1], schedules_two[0])
        self.assertEqual(schedules[2], schedules_tree[0])

    def test_get_ordered_schedules_home(self):
        """
        Tests if the schedules are returned ordered by date at get home.
        """
        review_one, review_two, review_tree = review_recipe.make(_quantity=3)
        schedules_one = c_schedules(calc_date_before, review_one, [5])
        schedules_two = c_schedules(calc_date_before, review_two, [6])
        schedules_tree = c_schedules(calc_date_before, review_tree, [7])
        response = self.client.get(reverse("home"))
        response_schedules = response.context['schedules']
        self.assertEqual(response_schedules[0], schedules_one[0])
        self.assertEqual(response_schedules[1], schedules_two[0])
        self.assertEqual(response_schedules[2], schedules_tree[0])

    def test_forgot_question(self):
        """
        Tests if a question atribute forgot is updated.
        """
        question_pk = question_recipe.make(forgot=False).pk
        self.client.post(reverse('forgot_question', kwargs={'pk': question_pk}))
        question = Question.objects.get(pk=question_pk)
        self.assertTrue(question.forgot)
