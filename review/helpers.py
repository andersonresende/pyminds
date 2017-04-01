import datetime

from templated_email import send_templated_mail

from review.models import Tag, Review, Question, Schedule


def _clean_tag_name(tag_name):
    return tag_name.lower().strip()


def create_tags(question, tags):
    if tags and question:
        for tag in tags.split(','):
            tag, _ = Tag.objects.get_or_create(name=_clean_tag_name(tag))
            question.tags.add(tag)


def create_schedules(review, *args):
    today = datetime.datetime.today()
    for d in args:
        schedule = Schedule(
            date=today + datetime.timedelta(d), review=review
        )
        schedule.save()


def create_review(questions):
    review = Review()
    review.save()
    for q in questions:
        q.review = review
        q.save()
    return review


def create_all():
    questions = Question.objects.filter(review=None)
    if questions.count() == 5:
        review = create_review(questions)
        create_schedules(review, 5, 15, 35, 60, 90)


def _normalize_and_split_data(text):
    # Remove first and last itens and split the string into a list.
    text = text.strip()
    last_open_sqbra = text.rfind('[')
    message = text
    categories_str = ''
    if text.endswith(']') and last_open_sqbra != -1:
        categories_str = text[last_open_sqbra + 1:-1]
        message = text[:last_open_sqbra]
    return message.strip(), categories_str


def send_review_email():
    schedules = Schedule.objects.to_send()
    for schedule in schedules:
        send_templated_mail(
            template_name='review',
            from_email='from@example.com',
            recipient_list=['to@example.com'],
            context={
                # 'username':request.user.username,
                # 'full_name':request.user.get_full_name(),
                # 'signup_date':request.user.date_joined
            },
        )
    Schedule.objects.update_to_emailed()
