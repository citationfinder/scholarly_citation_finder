from django.conf.urls import url

import views


urlpatterns = [
    url(r'^crossref/$', views.crossref),
    url(r'^duckduckgo/$', views.duckduckgo),
    url(r'^htmlparser/$', views.htmlparser),
]
