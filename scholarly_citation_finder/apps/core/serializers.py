from rest_framework import serializers

from models import *

class AffilationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Affilation
        #fields = ('id', 'name')


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
