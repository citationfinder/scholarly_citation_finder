from django.conf.urls import url

import views


urlpatterns = [
    url(r'^htmlparser/$', views.htmlparser, name='htmlparser'),
    url(r'^duckduckgo/$', views.duckduckgo, name='duckduckgo'),
    #url(r'^$', views.crawler_index, name='index'),
]
