from django.shortcuts import render
from django.http import HttpResponse

from .DblpHarvesterProcess import DblpHarvesterProcess

import logging

logger = logging.getLogger()

DBLP_DIR = 'downloads/dblp/'
DBLP_FILE_XML = 'dblp.xml'

def citeseerx_index(request):
    pass
    #harvester = CiteseerxHarvester()
    #harvester.harvest()
    #return HttpResponse("Hello, world. You're at the polls index.")
    
def dblp_index(request):
    logger.debug('dblp_index')
    #DblpDatabaseDownloader()
    try:
        process = DblpHarvesterProcess()
        process.harvest()
    except(Exception) as e:
        logger.warn(str(e))
    return HttpResponse("Hello, world. You're at the polls index.")