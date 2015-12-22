from django.conf.urls import include, url


urlpatterns = [
    url(r'^crawler/', include('search_for_citations.apps.api.crawler.urls')),
    url(r'^extractor/', include('search_for_citations.apps.api.extractor.urls')),
    url(r'^harvester/', include('search_for_citations.apps.api.harvester.urls')),
    url(r'^storage/', include('search_for_citations.apps.api.storage.urls'))
]
