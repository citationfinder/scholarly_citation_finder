from django.http import HttpResponse

from .PdfFinder import PdfFinder
from scholarly_citation_finder.api.crawler.Crawler import Crawler


def pdffinder_index(request):
    url = request.GET.get('url', None)

    if url:
        finder = PdfFinder()
        pdf = finder.get_pdf(url)
        return HttpResponse(pdf)
    else:
        return HttpResponse('Nothing do to. Usage: ?url=url')

def crawler_index(request):
    
    publication_id = request.GET.get('id', None)
    if publication_id:
        crawler = Crawler()
        crawler.run_by_id(publication_id)
        return HttpResponse('done')
    else:
        return HttpResponse('Nothing do to. Usage: ?id=publication-id')