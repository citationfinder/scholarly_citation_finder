from django.conf.urls import url

from citation import views as citation_views
from crawler import views as crawler_views
from extractor import views as extractor_views

urlpatterns = [
    url(r'^citation/$', citation_views.index, name='citation_index'),
    url(r'^crawler/htmlparser/$', crawler_views.htmlparser, name='crawler_htmlparser'),
    url(r'^crawler/duckduckgo/$', crawler_views.duckduckgo, name='crawler_duckduckgo'),
    url(r'^crawler/$', crawler_views.crawler_index, name='crawler_index'),
    url(r'^extractor/$', extractor_views.grobid_index, name='extractor_grobid_index')    
]
