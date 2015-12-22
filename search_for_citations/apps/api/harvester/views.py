from django.http import HttpResponse

from .DblpHarvesterProcess import DblpHarvesterProcess
from .CiteseerxHarvesterProcess import CiteseerxHarvesterProcess
from .ArxivHarvesterProcess import ArxivHarvesterProcess


def _get_params(request):
    return {'limit': request.GET.get('limit', None),
            'from': request.GET.get('from', None),
            'until': request.GET.get('until', None)}

    
def citeseerx_index(request):
    process = CiteseerxHarvesterProcess()
    r = process.harvest(_get_params(request))
    return HttpResponse('Start {}'.format(r))


def dblp_index(request):
    process = DblpHarvesterProcess()
    r= process.harvest(_get_params(request))
    return HttpResponse('Start {}'.format(r))


def arxiv_index(request):
    process = ArxivHarvesterProcess()
    r = process.harvest(_get_params(request))
    return HttpResponse('Start {}'.format(r))
