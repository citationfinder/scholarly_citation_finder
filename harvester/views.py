from django.shortcuts import render
from django.http import HttpResponse

from .dblp.DblpHarvester import DblpHarvester
from .dblp.DblpDatabaseDownloader import DblpDatabaseDownloader
from .citeseerx.CiteseerxHarvester import CiteseerxHarvester

import logging

logger = logging.getLogger()

DBLP_DIR = 'downloads/dblp/'
DBLP_FILE_XML = 'dblp.xml'

def citeseerx_index(request):
    harvester = CiteseerxHarvester()
    harvester.harvest()
    return HttpResponse("Hello, world. You're at the polls index.")
    
def dblp_index(request):
    logger.debug('dblp_index')
    #DblpDatabaseDownloader()
    harvester = DblpHarvester()
    #harvester.harvest(DBLP_DIR + DBLP_FILE_XML)
    harvester.harvest('test/dblp/dblp_medium.xml')
    return HttpResponse("Hello, world. You're at the polls index.")