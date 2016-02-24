#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from scholarly_citation_finder.api.citation.strategy.AuthorStrategy import AuthorStrategy
from scholarly_citation_finder.api.citation.strategy.ConferenceStrategy import ConferenceStrategy
from scholarly_citation_finder.api.citation.CitationFinder import CitationFinder
from django.utils.html import escape
import os.path
from scholarly_citation_finder import config
from scholarly_citation_finder.lib.process import external_process,\
    ProcessException


def _tail_file(filename, num_lines=10):
    try:
        exit_status, stdout, stderr = external_process(['tail', '-n', str(num_lines), filename])
        if exit_status == 0:
            return HttpResponse(escape(stdout))
        else:
            return HttpResponse(stderr, status=503)
    except(ProcessException) as e:
        return HttpResponse(str(e), status=503)    

def evaluation_status(request, name):
    filename = os.path.join(config.DOWNLOAD_DIR, 'evaluation', name, 'info.log')
    if not os.path.isfile(filename):
        return HttpResponse('evaluation with name {} does not exists'.format(name), status=404)
    return _tail_file(filename, 5)

def evaluation_authors(request, name):
    filename = os.path.join(config.DOWNLOAD_DIR, 'evaluation', name, 'authors.csv')
    if not os.path.isfile(filename):
        return HttpResponse('evaluation with name {} does not exists'.format(name), status=404)
    return _tail_file(filename, 105)

def index(request):
    author_name = request.GET.get('author_name', None)
    author_id = request.GET.get('author_id', None)
    
    if author_name or author_id:
        citation_finder = CitationFinder()
        citation_finder.set_by_author(name=author_name, id=author_id)
        
        citation_finder.run([AuthorStrategy(ordered=True, recursive=True, min_year=True)])        
        #citation_finder.run([AuthorStrategy(ordered=True, recursive=True, min_year=False),
        #                     JournalStrategy(ordered=True, min_year=True)])
        citation_finder.run([ConferenceStrategy(ordered=True, min_year=True)])
        return HttpResponse('Done')
    else:
        return HttpResponse('Nothing to do. Usage: ?author_name=<name> or ?author_id=<id>', status=400)
