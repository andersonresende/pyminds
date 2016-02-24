#! coding: utf-8

from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = patterns(
   '',
   url(r'^$', application_home, name='home'),
   url(r'^schedule/(.+)/$', schedule_page, name='schedule_page'),
   url(r'^questions/$', questions, name='questions'),
   url(r'^closed_questions/$', closed_questions, name='closed_questions'),
   url(r'^question/forgot/$', ForgotQuestionView.as_view(),
       name='forgot_question')
)