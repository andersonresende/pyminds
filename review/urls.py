from django.conf.urls import patterns, include, url
from django.conf import settings
from .views import *


urlpatterns = patterns(
    '',
   url (r'^$', application_home,name='home'),
   url(r'^schedule/(.+)/$', schedule_page, name='schedule_page'),
   url(r'^questions/$', questions, name='questions'),
    url(r'^closed_questions/$', closed_questions, name='closed_questions'),
)