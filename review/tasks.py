from pyminds import celery_app

from review.helpers import send_schedules_email


@celery_app.task
def hello_word_task():
    send_schedules_email()