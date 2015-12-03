from django.http import HttpResponse

from core.process_manager.Process import ExtractorProcess
from core.process_manager.utils import external_process2

class GrobidExtractorProcess(ExtractorProcess):
    
    PATH = "lib.extractor.grobid.GrobidExtractor"
    PARAM = '-l 2'    
    
    def extract(self, filename=None, filelist=None): 
        
        if filelist:
            external_process2(['python', '-m', self.PATH, self.PARAM, '-f {}'.format(filelist)]) 
            return HttpResponse("Start {} process".format(self.PATH))
        
        return HttpResponse("Nothing to do") 