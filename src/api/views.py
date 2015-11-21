from django.shortcuts import render
from django.http import HttpResponse
from search_for_citations.models import Publication

#from .extractor.CitationExtractor import CitationExtractor
from django.core.exceptions import ValidationError

from .harvester.DblpHarvesterProcess import DblpHarvesterProcess
from .harvester.CiteseerxHarvesterProcess import CiteseerxHarvesterProcess

def extractor_citeseer_index(request):
    
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