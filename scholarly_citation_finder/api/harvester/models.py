from django.db import models
from rest_framework import serializers, viewsets


class OaiPmhProvider(models.Model):
    
    name = models.CharField(max_length=50)
    url = models.URLField()
    identifier = models.CharField(max_length=50)

    def __unicode__(self):
        return unicode(self.name)
    
    
class OaiPmhProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OaiPmhProvider
        
        
class OaiPmhProviderViewSet(viewsets.ModelViewSet):
    queryset = OaiPmhProvider.objects.all()
    serializer_class = OaiPmhProviderSerializer