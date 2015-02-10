run:
	python manage.py runserver --settings pyminds.local_settings

test:
	python manage.py test review --settings pyminds.local_settings

shell:
	python manage.py shell --settings pyminds.local_settings
	
