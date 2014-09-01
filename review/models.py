import datetime
from django.db import models


class Review(models.Model):
	pass


class Schedule(models.Model):
    checked = models.BooleanField(default=False)
    rate = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    review = models.ForeignKey(Review)

    def __str__(self):
        return 'Schedule '+str(self.date)

    @staticmethod
    def get_current_shedules():
        today = datetime.datetime.today()
        schedules = Schedule.objects.filter(date__lte=today, checked=False)
        return schedules

    @staticmethod
    def get_next_schedule():
        today = datetime.datetime.today()
        schedules = Schedule.objects.filter(checked=False).exclude(date__lte=today).order_by('date')
        if schedules:
            return schedules[0]
        else:
            return None


class Question(models.Model):
    text = models.CharField(max_length=140, verbose_name="")
    date = models.DateTimeField(default=datetime.datetime.today())
    review = models.ForeignKey(Review, null=True,blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    questions = models.ManyToManyField(Question)