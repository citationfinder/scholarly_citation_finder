from django.shortcuts import render
from django.http import HttpResponse
from core.models import Publication
import requests

#from .extractor.CitationExtractor import CitationExtractor
from django.core.exceptions import ValidationError

from .harvester.DblpHarvesterProcess import DblpHarvesterProcess
from .harvester.CiteseerxHarvesterProcess import CiteseerxHarvesterProcess

from lib.extractor.citeseer.CiteseerExtractor import CiteseerExtractor

def extractor_citeseer_index(request):
    
    extractor = CiteseerExtractor()
    
    filename = request.GET.get('filename', None)
    if filename:
        extractor.extract_from_file(filename)
        return HttpResponse("Extract file")
    
    """
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
    """
    return HttpResponse("Hello, world. You're at the polls index.")

#import logging
#logger = logging.getLogger()

def harvester_citeseerx_index(request):
    process = CiteseerxHarvesterProcess()
    process.harvest()
    return HttpResponse("Start CiteseerxHarvester process")
    
def harvester_dblp_index(request):
    #logger.debug('dblp_index')
    #try:
    process = DblpHarvesterProcess()
    process.harvest()
    #except(Exception) as e:
    #    logger.warn(str(e))
    return HttpResponse("Start DblpHarvester process")