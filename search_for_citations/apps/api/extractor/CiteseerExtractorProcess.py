from django.http import HttpResponse

from ...core.process_manager.Process import ExtractorProcess
from ...core.process_manager.utils import external_process2


class CiteseerExtractorProcess(ExtractorProcess):

    PATH = 'search_for_citations.lib.extractor.citeseer'

    def extract(self, filename=None, filelist=None, limit=None):

        if filelist:
            process_args = ['python', '-m', self.PATH]
            if limit:
                process_args.append('-l {}'.format(limit))
            
            external_process2(process_args)
            return HttpResponse('Start {} process'.format(self.PATH))

        return HttpResponse('Nothing to do')
