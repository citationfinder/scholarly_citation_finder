from django.http.response import HttpResponse

from scholarly_citation_finder.api.extractor.grobid.GrobidExtractor import GrobidExtractor


def grobid_index(request):
    filename = request.GET.get('filename', None)
    if filename:
        extractor = GrobidExtractor()
        result = extractor.extract_file(filename)
        return HttpResponse(result)
    else:
        return HttpResponse('Nothing to do. Usage ?filename=<filename>')