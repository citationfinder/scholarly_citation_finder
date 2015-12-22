from django.http import HttpResponse

from .PdfFinder import PdfFinder

def pdffinder_index(request):
    url = request.GET.get('url', None)

    if url:
        finder = PdfFinder()
        pdf = finder.get_pdf(url)
        return HttpResponse(pdf)

    return HttpResponse('Nothing do to. Usage: ?url=<ULR>')