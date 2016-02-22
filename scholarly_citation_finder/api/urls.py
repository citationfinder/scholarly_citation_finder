from django.conf.urls import include, url

from extractor import views as extractor_views

urlpatterns = [
    url(r'^citation/', include('scholarly_citation_finder.api.citation.urls')),
    url(r'^crawler/', include('scholarly_citation_finder.api.crawler.urls')),
    url(r'^extractor/$', extractor_views.grobid_index, name='extractor_grobid_index')    
]
