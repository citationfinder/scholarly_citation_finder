#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from scholarly_citation_finder.api.citation import tasks
from scholarly_citation_finder.apps.tasks.models import Task
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

def evaluation_create(request, name):
    setsize = request.GET.get('setsize', None)
    num_min_publications = request.GET.get('num_min_publications', 0)
    if setsize:
        asyncresult = tasks.evaluation_create_author_set.delay(name=name, setsize=int(setsize), num_min_publications=int(num_min_publications))
        task = Task.objects.create(type=Task.TYPE_EVALUATION_SET, taskmeta_id=asyncresult.id)
        return JsonResponse(task.as_dict())
    else:
        return HttpResponse(status=400)

    
def evaluation_detail(request, id):
    try:
        task = Task.objects.get(pk=id)
        result, tastmeta = task.result()
        if result:
            with open(result) as result_file:
                return HttpResponse(result_file)
        else:
            return JsonResponse(tastmeta)
    except(ObjectDoesNotExist):
        return HttpResponse('Task #{} not found'.format(id), status=404)


def evaluation_run(request, name):
    asyncresult = tasks.evaluation_run.delay(name=name)
    task = Task.objects.create(type=Task.TYPE_EVALUATION_RUN, taskmeta_id=asyncresult.id)
    return JsonResponse(task.as_dict())
