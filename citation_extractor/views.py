from django.shortcuts import render

from django.http import HttpResponse
from search_for_citations.models import Publication

from .CiteSeerExtractor.CitationExtractor import CitationExtractor

def index(request):
    
    for publication in Publication.objects.filter(source__endswith='.pdf'):
        try:
            CitationExtractor(publication).extract(str(publication.source))
        except Exception as e:
            print(str(e))
        break
    
    return HttpResponse("Hello, world. You're at the polls index.")