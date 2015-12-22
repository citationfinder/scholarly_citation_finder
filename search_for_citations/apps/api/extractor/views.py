from django.http.response import HttpResponse

from ...core.process_manager.Process import ExtractorProcess


def _run_process(request, module):
    params = {'filename': request.GET.get('filename', None),
            'filelist': request.GET.get('filelist', None),
            'limit': request.GET.get('limit', None)}

    process = ExtractorProcess()
    process_args = process.run(['python', '-m', module], params)
    return HttpResponse('Start {}'.format(process_args))


def citeseer_index(request):
    return _run_process(request, 'search_for_citations.lib.extractor.citeseer')


def grobid_index(request):
    return _run_process(request, 'search_for_citations.lib.extractor.grobid')
