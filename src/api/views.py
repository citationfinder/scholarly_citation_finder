from django.shortcuts import render
from django.http import HttpResponse
from core.models import Publication
import requests

#from .extractor.CitationExtractor import CitationExtractor
from django.core.exceptions import ValidationError

from .harvester.DblpHarvesterProcess import DblpHarvesterProcess
from .harvester.CiteseerxHarvesterProcess import CiteseerxHarvesterProcess
from .extractor.CiteseerExtractorProcess import CiteseerExtractorProcess

def extractor_citeseer_index(request):
    # http://localhost:8000/api/extractor/citeseer?filename=../test/paper/OJWT_2014v1i2n02_Kusserow.pdf
    # http://localhost:8000/api/extractor/citeseer?filelist=../downloads/harvester/citeseerx/publication-0.xml
    process = CiteseerExtractorProcess()
    return process.extract(request.GET.get('filename', None), request.GET.get('filelist', None) )

def harvester_citeseerx_index(request):
    process = CiteseerxHarvesterProcess()
    process.harvest()
    return HttpResponse("Start CiteseerxHarvester process")
    
def harvester_dblp_index(request):
    process = DblpHarvesterProcess()
    process.harvest()
    return HttpResponse("Start DblpHarvester process")