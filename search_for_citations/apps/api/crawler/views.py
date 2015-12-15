from django.http import HttpResponse

from .GoogleScholar import GoogleScholar
from .PdfFinder import PdfFinder

def googlescholar_index(request):
    title = request.GET.get('title', None)

    if title:
        crawler = GoogleScholar()
        pdf = crawler.get_pdf(title)
        return HttpResponse(pdf)

    return HttpResponse('Nothing to do. Usage: ?title=<TITLE>')


def pdffinder_index(request):
    url = request.GET.get('url', None)

    if url:
        finder = PdfFinder()
        pdf = finder.get_pdf(url)
        return HttpResponse(pdf)

    return HttpResponse('Nothing do to. Usage: ?url=<ULR>')