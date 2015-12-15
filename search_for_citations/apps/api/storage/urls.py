from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^publications/$', views.publications_index, name='publications_index'),
    url(r'^coauthors/$', views.coauthors_index, name='coauthors_index')
]
