import datetime
from django.db import models


class ReviewManager(models.Manager):

    def closeds(self):
        """
        Return all closed reviews. Closed reviews
        are reviews without open schedules.
        """
        return self.exclude(
            pk__in=Schedule.objects.filter(
                checked=False
            ).values('review__pk'))


class Review(models.Model):

    objects = ReviewManager()

    def __str__(self):
        return 'Review %s' % self.pk


class ScheduleManager(models.Manager):

    def currents(self):
        """
        Return all schedules in progress.
        """
        return self.filter(
            date__lte=datetime.datetime.today(),
            checked=False
        ).order_by('review').distinct('review__id')


class Schedule(models.Model):
    class Meta:
        ordering = ['date']

    checked = models.BooleanField(default=False)
    rate = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    review = models.ForeignKey(Review, related_name='questions')

    objects = ScheduleManager()

    def __str__(self):
        return 'Schedule %s %s' % (self.review.pk, self.date.strftime("%d/%m/%Y"))

    @classmethod
    def close_last_schedules(cls, review):
        today = datetime.datetime.today()
        schedules = cls.objects.filter(date__lte=today, checked=False, review=review)
        schedules.update(checked=True)

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
    forgot = models.BooleanField(default=False)
    review = models.ForeignKey(Review, null=True, blank=True)

    @classmethod
    def get_all_closed_questions(cls):
        reviews_list = Review.objects.closeds()
        reviews_pk = [review.pk for review in reviews_list]
        questions_list = cls.objects.filter(review__pk__in=reviews_pk)
        return questions_list


class Tag(models.Model):

    class Meta:
        ordering = ['name']
    name = models.CharField(max_length=200)
    questions = models.ManyToManyField(Question)