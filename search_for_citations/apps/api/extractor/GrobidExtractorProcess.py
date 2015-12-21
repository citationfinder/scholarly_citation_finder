from django.http import HttpResponse

from ...core.process_manager.Process import ExtractorProcess
from ...core.process_manager.utils import external_process2


class GrobidExtractorProcess(ExtractorProcess):

    PATH = 'search_for_citations.lib.extractor.grobid'

    def extract(self, filename=None, filelist=None, limit=None):
        if filelist:
            process_args = ['python', '-m', self.PATH]
            process_args.append('-f {}'.format(filelist))            
            if limit:
                process_args.append('-l {}'.format(limit))
            
            external_process2(process_args)
            return HttpResponse('Start {} process'.format(self.PATH))

        return HttpResponse('Nothing to do')
