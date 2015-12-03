from .CiteseerExtractorProcess import CiteseerExtractorProcess
from .GrobidExtractorProcess import GrobidExtractorProcess

def citeseer_index(request):
    # http://localhost:8000/api/extractor/citeseer?filename=../test/paper/OJWT_2014v1i2n02_Kusserow.pdf
    # http://localhost:8000/api/extractor/citeseer?filelist=../downloads/harvester/citeseerx/publication-0.xml
    process = CiteseerExtractorProcess()
    return process.extract(request.GET.get('filename', None), request.GET.get('filelist', None) )

def grobid_index(request):
    process = GrobidExtractorProcess()
    return process.extract(request.GET.get('filename', None), request.GET.get('filelist', None) )