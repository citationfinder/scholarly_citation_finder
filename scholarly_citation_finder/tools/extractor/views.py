from django.http.response import HttpResponse, JsonResponse

from scholarly_citation_finder import config
from scholarly_citation_finder.tools.extractor.grobid.GrobidExtractor import GrobidExtractor
from scholarly_citation_finder.lib.file import download_file_pdf, DownloadFailedException, UnexpectedContentTypeException
from scholarly_citation_finder.tools.extractor.citeseer.CiteseerExtractor import CiteseerExtractor
from scholarly_citation_finder.lib.process import ProcessException
from scholarly_citation_finder.tools.extractor.grobid.TeiParser import TeiParserNoReferences,\
    TeiParserNoDocumentTitle
from scholarly_citation_finder.tools.extractor.Extractor import ExtractorNotAvaiableException


def grobid(request):
    filename = request.GET.get('filename', None)
    url = request.GET.get('url', None)    
    if filename or url:
        try:
            if url:
                filename = download_file_pdf(url, path=config.DOWNLOAD_TMP_DIR, name='tmp.pdf')
            extractor = GrobidExtractor()
            document_meta, references = extractor.extract_file(filename, completely=True)
            return JsonResponse({'item': {'document_meta': document_meta,
                                          'references': references}})
        # Tei failed -> invalid document
        except(TeiParserNoReferences, TeiParserNoDocumentTitle) as e:
            return HttpResponse(str(e), status=400)
        # Extractor failed
        except(ExtractorNotAvaiableException, ProcessException) as e:
            return HttpResponse(str(e), status=503)
        # Download failed
        except(DownloadFailedException, UnexpectedContentTypeException) as e:
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
        # Download failed
        except(DownloadFailedException, UnexpectedContentTypeException) as e:
            return HttpResponse(str(e), status=503)
        # Extractor failed
        except(ProcessException) as e:
            return HttpResponse(str(e), status=503)
    else:
        return HttpResponse('Nothing to do. Usage ?url=<url>', status=400)
