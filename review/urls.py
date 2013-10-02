from django.conf.urls import patterns, include, url
from django.conf import settings
from .views import application_home


urlpatterns = patterns(
    '',
    (r'^$', application_home,),
)
# if settings.DEBUG:
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += patterns('django.contrib.staticfiles.views',
#         url(r'^static/(?P<path>.*)$', 'serve'),
#     )
#     urlpatterns += patterns('',
#         url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#    )


# if settings.DEBUG:
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += patterns('django.contrib.staticfiles.views',
#         url(r'^static/(?P<path>.*)$', 'serve'),
#     )
#     urlpatterns += patterns('',
#         url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#    )