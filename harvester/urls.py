from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^citeseerx_index/$', views.citeseerx_index, name='citeseerx_index'),
    url(r'^dblp/$', views.dblp_index, name='dblp_index'),
]