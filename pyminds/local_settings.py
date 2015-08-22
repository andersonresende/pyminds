from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pyminds',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'local_user',
        'PASSWORD': '123',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5432',                      # Set to empty string for default.
    }
}
