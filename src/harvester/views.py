from django.shortcuts import render
from django.http import HttpResponse

from .DblpHarvesterProcess import DblpHarvesterProcess
from .CiteseerxHarvesterProcess import CiteseerxHarvesterProcess

#import logging
#logger = logging.getLogger()

def citeseerx_index(request):
    process = CiteseerxHarvesterProcess()
    process.harvest()
    return HttpResponse("Start CiteseerxHarvester process")
    
def dblp_index(request):
    #logger.debug('dblp_index')
    try:
        process = DblpHarvesterProcess()
        process.harvest()
    except(Exception) as e:
        logger.warn(str(e))
    return HttpResponse("Start DblpHarvester process")