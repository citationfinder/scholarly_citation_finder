#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from scholarly_citation_finder.api.citation.strategy.AuthorStrategy import AuthorStrategy
from scholarly_citation_finder.api.citation.strategy.JournalStrategy import JournalStrategy
from scholarly_citation_finder.api.citation.strategy.ConferenceStrategy import ConferenceStrategy
from scholarly_citation_finder.api.citation.CitationFinder import CitationFinder
from scholarly_citation_finder.api.citation.strategy.FieldofstudyStrategy import FieldofstudyStrategy
from scholarly_citation_finder.api.citation.PublicationSet import PublicationSet
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


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
        return HttpResponse('Nothing to do. Usage: ?author_name=<name> or ?author_id=<id>')


def author_detail(request):
    author_name = request.GET.get('author_name', None)
    if author_name:
        try:
            authors_publications = PublicationSet()
            authors_publications.set_by_author(name=author_name)            
            return JsonResponse({'min_year': authors_publications.get_min_year(),
                                 'authors': __serialize(authors_publications.get_authors())})
        except(ObjectDoesNotExist) as e:
            return HttpResponse(str(e), status=400)
        
def __serialize(array):
    result = []
    for item in array:
        result.append({'id': item.id, 'name': item.name})
    return result;