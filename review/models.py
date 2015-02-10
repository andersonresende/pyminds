import datetime
from django.db import models


class Review(models.Model):

    def is_closed(self):
        schedules_open = self.schedule_set.all().filter(checked=False).count()
        if schedules_open:
            return False
        return True

    def questions(self):
        return self.question_set.all()

    @classmethod
    def get_all_closed(cls):
        reviews_list = cls.objects.all()
        closed_reviews = [review for review in reviews_list if review.is_closed()]
        return closed_reviews

    def __str__(self):
        return 'Review %s' % self.pk


class Schedule(models.Model):
    class Meta:
        ordering = ['date']

    checked = models.BooleanField(default=False)
    rate = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    review = models.ForeignKey(Review)

    def __str__(self):
        return 'Schedule %s %s' % (self.review.pk, self.date.strftime("%d/%m/%Y"))

    @classmethod
    def close_last_schedules(cls, review):
        today = datetime.datetime.today()
        schedules = cls.objects.filter(date__lte=today, checked=False, review=review)
        schedules.update(checked=True)

    @classmethod
    def get_current_shedules(cls):
        today = datetime.datetime.today()
        schedules = cls.objects.filter(date__lte=today, checked=False)
        return schedules

    @classmethod
    def get_next_schedule(cls):
        today = datetime.datetime.today()
        schedules = cls.objects.filter(checked=False).exclude(date__lte=today)
        if schedules:
            return schedules[0]
        else:
            return None


class Question(models.Model):
    text = models.CharField(max_length=140, verbose_name="")
    date = models.DateTimeField(default=datetime.datetime.today())
    review = models.ForeignKey(Review, null=True,blank=True)

    @classmethod
    def get_all_closed_questions(cls):
        reviews_list = Review.get_all_closed()
        reviews_pk = [review.pk for review in reviews_list]
        questions_list = cls.objects.filter(review__pk__in=reviews_pk)
        return questions_list


class Tag(models.Model):

    class Meta:
        ordering = ['name']
    name = models.CharField(max_length=200)
    questions = models.ManyToManyField(Question)