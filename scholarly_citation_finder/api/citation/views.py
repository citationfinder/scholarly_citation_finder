#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from scholarly_citation_finder.api.citation.strategy.AuthorStrategy import AuthorStrategy
from scholarly_citation_finder.api.citation.strategy.JournalStrategy import JournalStrategy
from scholarly_citation_finder.api.citation.strategy.ConferenceStrategy import ConferenceStrategy
from scholarly_citation_finder.api.citation.CitationFinder import CitationFinder
from scholarly_citation_finder.api.citation.strategy.FieldofstudyStrategy import FieldofstudyStrategy
from django.utils.html import escape
import os.path
from scholarly_citation_finder import config
from scholarly_citation_finder.lib.process import external_process,\
    ProcessException

import tasks

def mag_authors_citations(request):
    author_id = request.GET.get('author_id', None)
    if author_id:
        tasks.mag_authors_citations.delay(author_id)
        return HttpResponse('started')
    else:
        return HttpResponse('Nothing to do. Usage: ?author_id=id', status=400)
"""
def evaluation_create(request):
    tasks.create_evaluation.delay('fu', 2, 0)
    return HttpResponse('started')
"""
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
        
        citation_finder.run([AuthorStrategy(ordered=True, min_year=True)])
        citation_finder.run([AuthorStrategy(ordered=True, recursive=True, min_year=True)])
        
        #citation_finder.run([AuthorStrategy(ordered=True, recursive=True, min_year=False),
        #                     JournalStrategy(ordered=True, min_year=True)])
        #citation_finder.run(JournalStrategy())
        #citation_finder.run(JournalStrategy(ordered=True))
        #citation_finder.run(JournalStrategy(ordered=True, min_year=True))
        citation_finder.run([ConferenceStrategy(ordered=True, min_year=True)])
        #citation_finder.run(FieldofstudyStrategy())
        #citation_finder.run(FieldofstudyStrategy(ordered=True))
        #citation_finder.run(FieldofstudyStrategy(ordered=True, limit=5))
        return HttpResponse('Done')
    else:
        return HttpResponse('Nothing to do. Usage: ?author_name=<name> or ?author_id=<id>', status=400)

"""
def author_detail(request):
    author_name = request.GET.get('author_name', None)
    if author_name:
        try:
            authors = Author.objects.using('mag').filter(name__contains=author_name)
            return JsonResponse({'items': __serialize(authors)})
        except(ObjectDoesNotExist) as e:
            return HttpResponse(str(e), status=400)
        
def __serialize(array):
    result = []
    for item in array:
        result.append({'id': item.id, 'name': item.name})
    return result;
"""