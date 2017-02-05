from django.conf.urls import include, url


urlpatterns = [
    url(r'', include('review.urls', namespace='review')),
    url(r'', include('review.endpoint_urls', namespace='review-endpoints')),
]
