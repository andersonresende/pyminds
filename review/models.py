import datetime
from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=140, verbose_name="")
    date = models.DateTimeField(default=datetime.datetime.today())


