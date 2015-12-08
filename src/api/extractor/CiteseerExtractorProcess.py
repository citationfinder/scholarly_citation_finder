from django.http import HttpResponse
#from lib.extractor.citeseer.CiteseerExtractor import CiteseerExtractor

from core.process_manager.Process import ExtractorProcess
from core.process_manager.utils import external_process2

class CiteseerExtractorProcess(ExtractorProcess):
    
    PATH = 'lib.extractor.citeseer'
    PARAM = '-l 2'    
    
    def extract(self, filename=None, filelist=None): 
        
        if filelist:
            external_process2(['python', '-m', self.PATH, self.PARAM, '-f {}'.format(filelist)]) 
            return HttpResponse('Start {} process'.format(self.PATH))
        """
        extractor = CiteseerExtractor() 
        
        if filename:
            extractor.extract_from_file(filename)
            return HttpResponse("Extract file")
        elif filelist:
            extractor.extract_from_xml_file(str(filelist))
            return HttpResponse("Extract list")
        """
        return HttpResponse('Nothing to do') 