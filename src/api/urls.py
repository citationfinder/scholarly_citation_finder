from django.conf.urls import include, url

urlpatterns = [
    url(r'^extractor/', include('api.extractor.urls')),
    url(r'^harvester/', include('api.harvester.urls')),
]