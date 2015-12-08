from django.http import HttpResponse

from .DblpHarvesterProcess import DblpHarvesterProcess
from .CiteseerxHarvesterProcess import CiteseerxHarvesterProcess
from .ArxivHarvesterProcess import ArxivHarvesterProcess

def citeseerx_index(request):
    process = CiteseerxHarvesterProcess()
    process.harvest()
    return HttpResponse('Start CiteseerxHarvester process')
    
def dblp_index(request):
    process = DblpHarvesterProcess()
    process.harvest()
    return HttpResponse('Start DblpHarvester process')

def arxiv_index(request):
    process = ArxivHarvesterProcess()
    process.harvest()
    return HttpResponse('Start ArxivHarvester process')   