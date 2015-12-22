from django.http import HttpResponse

from ...core.process_manager.Process import HarvesterProcess


def _run_process(request, module):
    params = {'limit': request.GET.get('limit', None),
            'from': request.GET.get('from', None),
            'until': request.GET.get('until', None)}

    process = HarvesterProcess()
    process_args = process.run(['python', '-m', module], params)
    return HttpResponse('Start {}'.format(process_args))

    
def citeseerx_index(request):
    return _run_process(request, 'search_for_citations.lib.harvester.citeseerx')


def dblp_index(request):
    return _run_process(request, 'search_for_citations.lib.harvester.dblp')


def arxiv_index(request):
    return _run_process(request, 'search_for_citations.lib.harvester.arxiv')
