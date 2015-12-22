from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^arxiv/$', views.arxiv_index, name='arxiv_index'),
    url(r'^citeseerx/$', views.citeseerx_index, name='citeseerx_index'),
    url(r'^dblp/$', views.dblp_index, name='dblp_index')
]
