from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^pdffinder/$', views.pdffinder_index, name='pdffinder_index')
]
