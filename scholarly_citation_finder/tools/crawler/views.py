from django.http import HttpResponse, JsonResponse
from requests.exceptions import ConnectionError

from .HtmlParser import HtmlParser
from .Duckduckgo import Duckduckgo, DuckduckgoResponseException
from .HtmlParser import HtmlParserUnkownHeaderType
from .Crossref import Crossref, CrossrefResponseException


def htmlparser(request):
    url = request.GET.get('url', None)
    if url:
        html_parser = HtmlParser()
        try:
            return JsonResponse({'results': html_parser.find_pdf_hyperrefs(url)})
        except(ConnectionError, HtmlParserUnkownHeaderType) as e:
            return HttpResponse(str(e), status=503)
    else:
        return HttpResponse('Nothing do to. Usage: ?url=url', status=400)


def duckduckgo(request):
    keywords = request.GET.get('keywords', None)
    if keywords:
        search_engine = Duckduckgo()
        try:
            return JsonResponse({'results': search_engine.query(keywords, filetype='pdf', limit=2)})
        except(ConnectionError, DuckduckgoResponseException) as e:
            return HttpResponse(str(e), status=503)
    else:
        return HttpResponse('Nothing do to. Usage: ?keywords=keywords', status=400)
    
    
def crossref(request):
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
    except(ConnectionError, CrossrefResponseException) as e:
        return HttpResponse(str(e), status=503)
