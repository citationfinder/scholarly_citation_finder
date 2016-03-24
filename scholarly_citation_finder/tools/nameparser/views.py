from django.http import HttpResponse, JsonResponse

from .AuthorNameParser import AuthorNameParser
from scholarly_citation_finder.tools.nameparser import StringMatching


def humanname(request):
    name = request.GET.get('name', None)
    normalize = request.GET.get('normalize', 'false') == 'true'
    if name:
        return JsonResponse({'item': AuthorNameParser(name, normalize=normalize).as_dict()})
    else:
        return HttpResponse('Nothing do to', status=400)
    

def stringmatching(request):
    first = request.GET.get('first', None)
    second = request.GET.get('second', None)
    if first and second:
        return JsonResponse({'item': {'ratio': StringMatching.match_ratio(first, second)}})
    else:
        return HttpResponse('Nothing do to', status=400)
 