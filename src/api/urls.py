from django.conf.urls import include, url

urlpatterns = [
    url(r'^crawler/', include('api.crawler.urls')),
    url(r'^extractor/', include('api.extractor.urls')),
    url(r'^harvester/', include('api.harvester.urls')),
    url(r'^storage/', include('api.storage.urls'))
]
