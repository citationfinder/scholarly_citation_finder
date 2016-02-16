from django.conf.urls import url

from citation import views as citation_views
from crawler import views as crawler_views
from extractor import views as extractor_views

urlpatterns = [
    url(r'^citation/$', citation_views.index, name='citation_index'),
    url(r'^crawler/pdffinder/$', crawler_views.pdffinder_index, name='crawler_pdffinder_index'),
    url(r'^crawler/crawler/$', crawler_views.crawler_index, name='crawler_crawler_index'),    
    url(r'^extractor/$', extractor_views.grobid_index, name='extractor_grobid_index')    
]
