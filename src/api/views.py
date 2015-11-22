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
    
    # http://localhost:8000/api/extractor/citeseer?filename=../test/paper/OJWT_2014v1i2n02_Kusserow.pdf
    filename = request.GET.get('filename', None)
    # http://localhost:8000/api/extractor/citeseer?filename=../downloads/harvester/citeseerx/publication-0.xml
    filelist = request.GET.get('filelist', None)    
    if filename:
        extractor.extract_from_file(filename)
        return HttpResponse("Extract file")
    elif filelist:
        extractor.extract_from_xml_file(str(filelist))
        return HttpResponse("Extract list")        
    

    return HttpResponse("Nothing to do")

#import logging
#logger = logging.getLogger()

def harvester_citeseerx_index(request):
    process = CiteseerxHarvesterProcess()
    process.harvest()
    return HttpResponse("Start CiteseerxHarvester process")
    
def harvester_dblp_index(request):
    process = DblpHarvesterProcess()
    process.harvest()
    return HttpResponse("Start DblpHarvester process")