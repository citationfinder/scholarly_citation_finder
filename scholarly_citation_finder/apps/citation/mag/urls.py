from django.conf.urls import url

import views


urlpatterns = [
    url(r'^(?P<id>[0-9]+)/$', views.task_detail),
    url(r'^$', views.index),
]
