from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^citeseer/$', views.citeseer_index, name='citeseer_index'),
]