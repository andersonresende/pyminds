from .base import *  # noqa


HOST = 'http://localhost:8000'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Slack integration
SLACK_TOKEN_API = 'slacktoken123'

# Celery
CELERY_TASK_ALWAYS_EAGER = True

# Email
INSTALLED_APPS += ('naomi',)
EMAIL_BACKEND = 'naomi.mail.backends.naomi.NaomiBackend'
EMAIL_FILE_PATH = base_dir_join('tmp_email')
