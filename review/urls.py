from django.conf.urls import patterns, include, url
from django.conf import settings
from .views import application_home, schedule_page


urlpatterns = patterns(
    '',
   url (r'^$', application_home,),
    url(r'^schedule/(.+)/$', schedule_page, name='schedule_page'),
)