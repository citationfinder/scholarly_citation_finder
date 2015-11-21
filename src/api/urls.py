from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^extractor/citeseer$', views.extractor_citeseer_index, name='extractor_citeseer_index'),
    url(r'^harvester/citeseerx/$', views.harvester_citeseerx_index, name='harvester_citeseerx_index'),
    url(r'^harvester/dblp/$', views.harvester_dblp_index, name='harvester_dblp_index'),
]