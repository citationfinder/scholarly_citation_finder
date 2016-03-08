from django.http.response import HttpResponse, JsonResponse

from scholarly_citation_finder import config
from scholarly_citation_finder.api.extractor.grobid.GrobidExtractor import GrobidExtractor
from scholarly_citation_finder.lib.file import download_file_pdf,\
    DownloadPdfException
from scholarly_citation_finder.api.extractor.citeseer.CiteseerExtractor import CiteseerExtractor
from scholarly_citation_finder.lib.process import ProcessException


def grobid(request):
    filename = request.GET.get('filename', None)
    url = request.GET.get('url', None)    
    if filename or url:
        try:
            if url:
                filename = download_file_pdf(url, path=config.DOWNLOAD_TMP_DIR, name='tmp.pdf')
            extractor = GrobidExtractor()
            result = extractor.extract_file(filename)
            return JsonResponse({'items': result})
        except(DownloadPdfException) as e:
            return HttpResponse(str(e), status=503)
    else:
        return HttpResponse('Nothing to do. Usage ?filename=<filename> or ?url=<url>', status=400)


def citeseer(request):
    url = request.GET.get('url', None)    
    if url:
        try:
            filename = download_file_pdf(url, path=config.DOWNLOAD_TMP_DIR, name='tmp.pdf')
            extractor = CiteseerExtractor()
            result = extractor.extract_file(filename)
            return JsonResponse({'items': result})
        except(DownloadPdfException, ProcessException) as e:
            return HttpResponse(str(e), status=503)
    else:
        return HttpResponse('Nothing to do. Usage ?url=<url>', status=400)
