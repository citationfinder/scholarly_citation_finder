from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^citeseer$', views.citeseer_index, name='citeseer_index'),
]