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


class ScheduleQuerySet(models.QuerySet):

    def update_to_emailed(self):
        return self.to_send_email().update(emailed=True)

    def to_send_email(self):
        """
        Return the schedules to send over email
        """
        return self.filter(
            date__lte=datetime.datetime.today(),
            emailed=False
        )

    def currents(self):
        """
        Return the schedules in progress.
        """
        return self.filter(
            date__lte=datetime.datetime.today(),
            checked=False
        ).order_by('review').distinct('review__id')


class Schedule(models.Model):
    class Meta:
        ordering = ['date']

    checked = models.BooleanField(default=False)
    emailed = models.BooleanField(default=False)
    rate = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    review = models.ForeignKey(Review, related_name='questions')

    objects = ScheduleQuerySet.as_manager()

    def __str__(self):
        return 'Schedule {} {}'.format(
            self.review.pk,
            self.date.strftime("%d/%m/%Y")
        )

    @classmethod
    def close_last_schedules(cls, review):
        today = datetime.datetime.today()
        schedules = cls.objects.filter(
            date__lte=today,
            checked=False,
            review=review
        )
        schedules.update(checked=True)

    @classmethod
    def get_next_schedule(cls):
        today = datetime.datetime.today()
        schedules = cls.objects.filter(checked=False).exclude(date__lte=today)
        if schedules:
            return schedules[0]
        else:
            return None


class QuestionManager(models.Manager):

    def closeds(self):
        """
        Return the questions with closed reviews.
        """
        return self.filter(review__in=Review.objects.closeds())


class Question(models.Model):
    text = models.CharField(max_length=140, verbose_name="")
    date = models.DateTimeField(default=datetime.datetime.today())
    forgot = models.BooleanField(default=False)
    reference_link = models.URLField(blank=True, verbose_name="")
    review = models.ForeignKey(Review, null=True, blank=True)

    objects = QuestionManager()

    def update_forgot(self):
        self.forgot = True
        self.save()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    questions = models.ManyToManyField(Question, related_name='tags')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return 'Review {}'.format(self.name)
