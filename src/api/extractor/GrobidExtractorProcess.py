from django.http import HttpResponse

from core.process_manager.Process import ExtractorProcess
from core.process_manager.utils import external_process2


class GrobidExtractorProcess(ExtractorProcess):

    PATH = 'lib.extractor.grobid'

    def extract(self, filename=None, filelist=None, limit=None):

        if filelist:
            params = ''
            if limit:
                params += '-l {}'.format(limit)
            
            external_process2(['python', '-m', self.PATH, params])
            return HttpResponse('Start {} process'.format(self.PATH))

        return HttpResponse('Nothing to do')
