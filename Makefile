run:
	python manage.py runserver --settings pyminds.settings.local

test:
	python manage.py test review --settings pyminds.settings.test

shell:
	python manage.py shell --settings pyminds.settings.local
	
