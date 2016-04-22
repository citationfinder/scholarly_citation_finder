#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse

from scholarly_citation_finder.apps.citation.mag import tasks
from scholarly_citation_finder.apps.tasks.models import Task


def index(request):
    type = request.GET.get('type', None)
    name = request.GET.get('name', None)
    id = request.GET.get('id', None)
    if type in ('author', 'conference', 'journal') and (name or id):
        publin_callback_url=request.GET.get('publin_callback_url', None)
        isi_fieldofstudy = request.GET.get('fieldofstudy', None) == 'isi'
        asyncresult = tasks.citations.delay(type=type,
                                            name=name,
                                            id=int(id) if id else None,
                                            publin_callback_url=publin_callback_url,
                                            isi_fieldofstudy=isi_fieldofstudy)
        task = Task.objects.create(type=Task.TYPE_CITATION_MAG, taskmeta_id=asyncresult.id)
        return JsonResponse(task.as_dict())
    else:
        return HttpResponse('Nothing to do', status=400)


def task_detail(request, id):
    try:
        task = Task.objects.get(pk=id)
        result, tastmeta = task.result()
        if result and os.path.isfile(result):
            with open(result) as result_file:
                return HttpResponse(result_file, content_type='application/json')
        elif result:
            return HttpResponse(result)
        else:
            return JsonResponse(tastmeta)
    except(ObjectDoesNotExist):
        return HttpResponse('Task #{} not found'.format(id), status=404)
