from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^googlescholar/$', views.googlescholar_index, name='googlescholar_index'),
    url(r'^pdffinder/$', views.pdffinder_index, name='pdffinder_index')
]
