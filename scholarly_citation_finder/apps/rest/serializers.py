from rest_framework import serializers

from scholarly_citation_finder.apps.core.models import *

class AffilationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Affilation


class ConferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conference


class ConferenceInstanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConferenceInstance
        

class FieldOfStudySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FieldOfStudy

   
class JournalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Journal


class PublicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Publication
        
        
class PublicationAuthorAffilationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PublicationAuthorAffilation


class PublicationKeywordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PublicationKeyword
        

class PublicationReferencePublicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PublicationReference
        

class PublicationUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PublicationUrl
