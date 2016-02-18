from django.http.response import HttpResponse, JsonResponse
import os.path

from scholarly_citation_finder import config
from scholarly_citation_finder.api.extractor.grobid.GrobidExtractor import GrobidExtractor
from scholarly_citation_finder.lib.file import download_file_pdf,\
    UnexpectedContentTypeException
from requests.exceptions import InvalidSchema, ConnectionError

def grobid_index(request):
    filename = request.GET.get('filename', None)
    url = request.GET.get('url', None)    
    if filename or url:
        if url:
            try:
                filename = download_file_pdf(url, path=config.DOWNLOAD_TMP_DIR, name='tmp.pdf')
            except(UnexpectedContentTypeException, InvalidSchema, ConnectionError) as e:
                return HttpResponse(e.__type__, status=503)
        extractor = GrobidExtractor()
        result = extractor.extract_file(os.path.join(config.DOWNLOAD_TMP_DIR, filename))
        return JsonResponse({'items': result})
    else:
        return HttpResponse('Nothing to do. Usage ?filename=<filename> or ?url=<url>', status=400)