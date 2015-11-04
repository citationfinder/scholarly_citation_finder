from django.shortcuts import render

from django.http import HttpResponse

#from .lib.dblp_database_downloader import DblpDatabaseDownloader
from .lib.dblp_database_downloader import DblpDatabaseDownloader
#from .lib.dblp_parser import DblpParser

def index(request):
    #DblpDatabaseDownloader()
    #DblpParser()
    return HttpResponse("Hello, world. You're at the polls index.")