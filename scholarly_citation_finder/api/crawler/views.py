from django.http import HttpResponse, JsonResponse
from requests.exceptions import ConnectionError

from scholarly_citation_finder.api.crawler.search.HtmlParser import HtmlParser
from scholarly_citation_finder.api.crawler.search.Duckduckgo import Duckduckgo,\
    DuckduckgoResponseException
from scholarly_citation_finder.api.crawler.Crawler import Crawler
from scholarly_citation_finder.api.crawler.search.HtmlParser import HtmlParserUnkownHeaderType


def htmlparser(request):
    url = request.GET.get('url', None)
    if url:
        html_parser = HtmlParser()
        try:
            return JsonResponse({'items': html_parser.find_pdf_hyperrefs(url)})
        except(ConnectionError, HtmlParserUnkownHeaderType) as e:
            return JsonResponse({'msg': str(e)}, status=503)
    else:
        return JsonResponse({'msg': 'Nothing do to. Usage: ?url=url'}, status=400)


def duckduckgo(request):
    keywords = request.GET.get('keywords', None)
    if keywords:
        search_engine = Duckduckgo()
        try:
            return JsonResponse({'items': search_engine.query(keywords, filetype='pdf', limit=2)})
        except(ConnectionError, DuckduckgoResponseException) as e:
            return JsonResponse({'msg': str(e)}, status=503)
    else:
        return HttpResponse({'msg': 'Nothing do to. Usage: ?keywords=keywords'}, status=400)


def crawler_index(request):
    
    publication_id = request.GET.get('id', None)
    if publication_id:
        crawler = Crawler()
        crawler.run_by_id(publication_id)
        return HttpResponse('done')
    else:
        return HttpResponse('Nothing do to. Usage: ?id=publication-id')