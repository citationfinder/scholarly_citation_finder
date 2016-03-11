from django.db import models
from rest_framework import serializers, viewsets


class Harvester(models.Model):
    
    TYPE_OAI = 'oai'
    TYPE_OTHER = 'other'
    TYPES = [
        (TYPE_OAI, TYPE_OAI),
        (TYPE_OTHER, TYPE_OTHER)
    ]

    name = models.CharField(unique=True, max_length=50)
    type = models.CharField(max_length=50, choices=TYPES)
    oai_url = models.URLField(blank=True, null=True)
    oai_identifier = models.CharField(blank=True, null=True, max_length=50)

    def __unicode__(self):
        return unicode(self.name)
    
    
class HarvesterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Harvester
        
        
class HarvesterViewSet(viewsets.ModelViewSet):
    queryset = Harvester.objects.all()
    serializer_class = HarvesterSerializer
    
    def get_queryset(self):
        queryset = Harvester.objects.all()
        type = self.request.query_params.get('type', None)
        if type:
            queryset = self.queryset.filter(type=type)
        return queryset
