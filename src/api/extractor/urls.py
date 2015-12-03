from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^citeseer/$', views.citeseer_index, name='citeseer_index'),
    url(r'^grobid/$', views.grobid_index, name='grobid_index'),
]