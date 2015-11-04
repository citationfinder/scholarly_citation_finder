from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^author/(?P<author_id>[0-9]+)/$', views.author_details, name='author_details'),
]