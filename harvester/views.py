from django.shortcuts import render
from django.http import HttpResponse

from .dblp.DblpHarvester import DblpHarvester
from .dblp.DblpDatabaseDownloader import DblpDatabaseDownloader
from .citeseerx.CiteseerxHarvester import CiteseerxHarvester

def citeseerx_index(request):
    harvester = CiteseerxHarvester()
    harvester.harvest()
    return HttpResponse("Hello, world. You're at the polls index.")
    
def dblp_index(request):
    #DblpDatabaseDownloader()
    harvester = DblpHarvester()
    harvester.harvest()
    return HttpResponse("Hello, world. You're at the polls index.")