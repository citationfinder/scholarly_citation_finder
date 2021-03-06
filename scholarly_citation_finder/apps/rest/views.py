from rest_framework import viewsets
from scholarly_citation_finder.apps.core.models import Affilation, Conference, ConferenceInstance, FieldOfStudy, Journal, Publication, PublicationAuthorAffilation, PublicationKeyword, PublicationReference, PublicationUrl
from scholarly_citation_finder.apps.rest.serializers import *

DB_NAME = 'mag'

class AffiliationViewSet(viewsets.ModelViewSet):
    queryset = Affilation.objects.using(DB_NAME).all()
    serializer_class = AffilationSerializer


class ConferenceViewSet(viewsets.ModelViewSet):
    queryset = Conference.objects.using(DB_NAME).all()
    serializer_class = ConferenceSerializer


class ConferenceInstanceViewSet(viewsets.ModelViewSet):
    queryset = ConferenceInstance.objects.using(DB_NAME).all()
    serializer_class = ConferenceInstanceSerializer


class FieldOfStudyViewSet(viewsets.ModelViewSet):
    serializer_class = FieldOfStudySerializer
    queryset = FieldOfStudy.objects.using(DB_NAME).all()


class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.using(DB_NAME).all()
    serializer_class = JournalSerializer


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.using(DB_NAME).all()
    serializer_class = PublicationSerializer