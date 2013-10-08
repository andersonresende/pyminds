from django.conf.urls import patterns, include, url
from django.conf import settings
from .views import application_home


urlpatterns = patterns(
    '',
    (r'^$', application_home,),
)