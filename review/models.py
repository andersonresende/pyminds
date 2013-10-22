import datetime
from django.db import models


class Review(models.Model):
	pass


class Schedule(models.Model):
    checked = models.BooleanField(default=False)
    rate = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    review = models.ForeignKey(Review)

    @staticmethod
    def get_current_shedules():
        today = datetime.datetime.today()
        schedules = Schedule.objects.filter(date__let=today, checked=False)
        return schedules

class Question(models.Model):
    text = models.CharField(max_length=140, verbose_name="")
    date = models.DateTimeField(default=datetime.datetime.today())
    review = models.ForeignKey(Review, null=True,blank=True)


