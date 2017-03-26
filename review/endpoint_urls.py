#! coding: utf-8
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .endpoints import CreateQuestionEndpoint


urlpatterns = [
   url(r'^question/$', CreateQuestionEndpoint.as_view(), name='create-question'),
]
