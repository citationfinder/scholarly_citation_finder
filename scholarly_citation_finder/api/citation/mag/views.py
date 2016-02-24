#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from djcelery.models import TaskMeta
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse

from scholarly_citation_finder.api.citation.mag import tasks
from scholarly_citation_finder.apps.tasks.models import Task


def index(request):
    author_name = request.GET.get('author_name', None)
    author_id = request.GET.get('author_id', None)
    if author_name or author_id:
        asyncresult = tasks.citations.delay(author_name=author_name, author_id=author_id)
        task = Task.objects.create(type=Task.TYPE_CITATION_MAG, taskmeta_id=asyncresult.id)
        return JsonResponse({'id': task.id,
                             'url': '/api/citations/mag/{}/'.format(task.id),
                             'starttime': task.starttime})
    else:
        response_items = []
        for task in Task.objects.filter(type=Task.TYPE_CITATION_MAG):
            try:
                taskmeta = TaskMeta.objects.get(task_id=task.taskmeta_id)
                response_items.append({'id': task.id,
                               'starttime': task.starttime,
                               'status': taskmeta.status,
                               'traceback': taskmeta.traceback})
            except(ObjectDoesNotExist):
                pass
        return JsonResponse({'items': response_items})


def task_detail(request, id):
    try:
        taskmeta_id = Task.objects.get(pk=id).taskmeta_id
        tastmeta = TaskMeta.objects.get(task_id=taskmeta_id)
        with open(tastmeta.result) as result_file:
            return HttpResponse(result_file, content_type='application/json')
        return JsonResponse({'status': tastmeta.status,
                            'traceback': tastmeta.traceback,
                            'result': tastmeta.result,
                            'date_done': tastmeta.date_done})
    except(ObjectDoesNotExist):
        return HttpResponse('Task #{} not found'.format(id), status=404)
