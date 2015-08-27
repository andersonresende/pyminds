#! coding: utf-8

from django.conf.urls import patterns, include, url

from .views import *

urlpatterns = patterns(
   '',
   url(r'^$', application_home, name='home'),
   url(r'^schedule/(.+)/$', schedule_page, name='schedule_page'),
   url(r'^questions/$', questions, name='questions'),
   url(r'^closed_questions/$', closed_questions, name='closed_questions'),
   url(r'^unlearn_question/(?P<pk>\d+)/$', UnlearnQuestionView.as_view(), name='unlearn_question'),
)