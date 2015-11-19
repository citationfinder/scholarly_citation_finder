from django.shortcuts import render

from django.http import HttpResponse
from search_for_citations.models import Publication

from .citeseer.CitationExtractor import CitationExtractor
from django.core.exceptions import ValidationError

def citeseer_index(request):
    
    for publication in Publication.objects.filter(source__endswith='.pdf'):
        try:
            result = CitationExtractor(publication).extract()
            if result:
                publication.source_extracted = True
                publication.save()
            else:
                publication.source = None
                publication.save()
        except ValidationError:
            publication.source = None
            publication.save()
    
    return HttpResponse("Hello, world. You're at the polls index.")