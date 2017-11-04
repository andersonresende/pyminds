run:
	python manage.py runserver

test:
	python manage.py test review

shell:
	python manage.py shell

worker:
	celery --app=pyminds.celery worker --loglevel=info