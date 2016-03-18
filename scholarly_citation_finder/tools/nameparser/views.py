from django.http import HttpResponse, JsonResponse

from .AuthorNameParser import AuthorNameParser


def nameparser(request):
    name = request.GET.get('name', None)
    normalize = request.GET.get('normalize', 'false') == 'true'
    if name:
        return JsonResponse({'item': AuthorNameParser(name, normalize=normalize).as_dict()})
    else:
        return HttpResponse('Nothing do to', status=400)
