from django.http import HttpResponse
from lib.extractor.citeseer.CiteseerExtractor import CiteseerExtractor

class CiteseerExtractorProcess:
    
    def extract(self, filename=None, filelist=None):
        extractor = CiteseerExtractor()  
        if filename:
            extractor.extract_from_file(filename)
            return HttpResponse("Extract file")
        elif filelist:
            extractor.extract_from_xml_file(str(filelist))
            return HttpResponse("Extract list")
    
        return HttpResponse("Nothing to do") 