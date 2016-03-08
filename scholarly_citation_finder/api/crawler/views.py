from django.http import HttpResponse, JsonResponse
from requests.exceptions import ConnectionError

from scholarly_citation_finder.api.crawler.search.HtmlParser import HtmlParser
from scholarly_citation_finder.api.crawler.search.Duckduckgo import Duckduckgo,\
    DuckduckgoResponseException
from scholarly_citation_finder.api.crawler.PublicationCrawler import PublicationCrawler
from scholarly_citation_finder.api.crawler.search.HtmlParser import HtmlParserUnkownHeaderType
from scholarly_citation_finder.api.crawler.search.Crossref import Crossref, CrossrefResponseException
from django.core.exceptions import ObjectDoesNotExist


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
        

def crawler_index(request):
    publication_id = request.GET.get('id', None)
    if publication_id:
        try:
            crawler = PublicationCrawler()
            crawler.set_by_id(publication_id)
            return HttpResponse('done')
        except(ObjectDoesNotExist) as e:
            return HttpResponse('Publication does not exists', status=400)
    else:
        return HttpResponse('Nothing do to. Usage: ?id=publication-id', status=400)