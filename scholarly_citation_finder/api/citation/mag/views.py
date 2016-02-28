#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
from django.http import HttpResponse
from djcelery.models import TaskMeta
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse

from scholarly_citation_finder.api.citation.mag import tasks
from scholarly_citation_finder.apps.tasks.models import Task


def index(request):
    author_name = request.GET.get('author_name', None)
    author_id = request.GET.get('author_id', None)
    publin_callback_url = request.GET.get('publin_callback_url', None)
    if author_name or author_id:
        asyncresult = tasks.citations.delay(author_name=author_name, author_id=int(author_id), publin_callback_url=publin_callback_url)
        task = Task.objects.create(type=Task.TYPE_CITATION_MAG, taskmeta_id=asyncresult.id)
        return JsonResponse(task.as_dict())
    else:
        return HttpResponse(status=400)


def task_detail(request, id):
    try:
        task = Task.objects.get(pk=id)
        result, tastmeta = task.result()
        if os.path.isfile(result):
            with open(result) as result_file:
                return HttpResponse(result_file, content_type='application/json')
        elif result:
            return HttpResponse(result)
        else:
            return JsonResponse(tastmeta)
    except(ObjectDoesNotExist):
        return HttpResponse('Task #{} not found'.format(id), status=404)
