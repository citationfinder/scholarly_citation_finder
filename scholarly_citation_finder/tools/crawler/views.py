from django.http import HttpResponse, JsonResponse
from requests.exceptions import ConnectionError, Timeout

from .HtmlParser import HtmlParser
from .engine.SearchEngine import SearchEngineResponseException
from .engine.Duckduckgo import Duckduckgo
from .HtmlParser import HtmlParserUnkownHeaderType
from .Crossref import Crossref, CrossrefResponseException
from scholarly_citation_finder.tools.crawler.Crossref import CrossrefNothingFoundException,\
    CrossrefUnwantedType


def htmlparser(request):
    '''
    HTMLParser view.
    
    :param request: Django request
    '''
    url = request.GET.get('url', None)
    if url:
        html_parser = HtmlParser()
        try:
            hyperrefs, _ = html_parser.find_pdf_hyperrefs(url)
            return JsonResponse({'results': hyperrefs})
        except(ConnectionError, HtmlParserUnkownHeaderType) as e:
            return HttpResponse(str(e), status=503)
    else:
        return HttpResponse('Nothing do to. Usage: ?url=url', status=400)


def duckduckgo(request):
    '''
    DuckDuckGo view.
    
    :param request: Django request
    '''
    keywords = request.GET.get('keywords', None)
    if keywords:
        search_engine = Duckduckgo()
        try:
            return JsonResponse({'results': search_engine.query(keywords, filetype=search_engine.API_PARAM_FILETYPE_PDF, limit=2)})
        except(ConnectionError, Timeout, SearchEngineResponseException) as e:
            return HttpResponse(str(e), status=503)
    else:
        return HttpResponse('Nothing do to. Usage: ?keywords=keywords', status=400)
    
    
def crossref(request):
    '''
    CrossRef view.
    
    :param request: Django request
    '''
    query = request.GET.get('query', None)
    doi = request.GET.get('doi', None)
    try:
        search_engine = Crossref()
        if query:
            return JsonResponse({'results': search_engine.query_works(query=query)})
        elif doi:
            return JsonResponse({'item': search_engine.query_works_doi(doi)})
        else:
            return HttpResponse('Nothing do to', status=400)
    except(ConnectionError, CrossrefResponseException, CrossrefNothingFoundException, CrossrefUnwantedType) as e:
        return HttpResponse(str(e), status=503)
