from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^authors/$', views.authors_index, name='authors_index'),
    url(r'^authors/(?P<author_id>[0-9]+)/$', views.authors_details, name='authors_details'),
    url(r'^publications/(?P<source>[a-z]+|)$', views.publications_index, name='publications_index'),
    url(r'^publications/(?P<publication_id>[0-9]+)/$', views.publications_details, name='publications_details')
]
