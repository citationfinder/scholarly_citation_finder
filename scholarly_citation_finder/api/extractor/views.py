from django.http.response import HttpResponse, JsonResponse
import os.path

from scholarly_citation_finder import config
from scholarly_citation_finder.api.extractor.grobid.GrobidExtractor import GrobidExtractor
from scholarly_citation_finder.lib.file import download_file_pdf,\
    UnexpectedContentTypeException
from requests.exceptions import InvalidSchema, ConnectionError
from scholarly_citation_finder.api.extractor.citeseer.CiteseerExtractor import CiteseerExtractor
from scholarly_citation_finder.lib.process import ProcessException


def grobid(request):
    filename = request.GET.get('filename', None)
    url = request.GET.get('url', None)    
    if filename or url:
        if url:
            try:
                filename = __download_pdf(url)
            except(DownloadPdfException) as e:
                return HttpResponse(str(e), status=503)
        extractor = GrobidExtractor()
        result = extractor.extract_file(path=config.DOWNLOAD_TMP_DIR, filename=filename)
        return JsonResponse({'items': result})
    else:
        return HttpResponse('Nothing to do. Usage ?filename=<filename> or ?url=<url>', status=400)


def citeseer(request):
    url = request.GET.get('url', None)    
    if url:
        try:
            filename = __download_pdf(url)
            extractor = CiteseerExtractor()
            result = extractor.extract_file(path=config.DOWNLOAD_TMP_DIR, filename=filename)
            return JsonResponse({'items': result})
        except(DownloadPdfException, ProcessException) as e:
            return HttpResponse(str(e), status=503)
    else:
        return HttpResponse('Nothing to do. Usage ?url=<url>', status=400)
    

def DownloadPdfException(Exception):
    pass


def __download_pdf(url):
    try:
        return download_file_pdf(url, path=config.DOWNLOAD_TMP_DIR, name='tmp.pdf')
    except(UnexpectedContentTypeException, InvalidSchema, ConnectionError) as e:
        raise DownloadPdfException(e)