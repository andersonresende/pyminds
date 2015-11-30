from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pyminds',
        'USER': 'pyminds_user',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
