#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

import tasks
from scholarly_citation_finder.apps.tasks.models import Task
from .strategy.AuthorStrategy import AuthorStrategy
from .strategy.ConferenceStrategy import ConferenceStrategy
from .strategy.FieldofstudyStrategy import FieldofstudyStrategy
from .strategy.JournalStrategy import JournalStrategy
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def citations_find(request):
    '''
    Find citations view.
    
    :param request: Django request
    '''
    type = request.GET.get('type', None)
    name = request.GET.get('name', None)
    id = request.GET.get('id', None)
    if type in ('author', 'conference', 'journal') and (name or id):
        try:
            if request.body:
                strategy=eval(request.body)
            else:
                strategy = [AuthorStrategy(ordered=True)]

            asyncresult = tasks.citations_find.delay(type=type,
                                                     name=name,
                                                     id=int(id) if id else None,
                                                     strategy=strategy)
            task = Task.objects.create(type=Task.TYPE_CITATION_FIND, taskmeta_id=asyncresult.id)
            return JsonResponse(task.as_dict())
        except(AttributeError, SyntaxError, TypeError) as e:
            return HttpResponse('Strategies string is not valid. {}: {}'.format(e.__class__.__name__, str(e)), status=400)
    else:
        return HttpResponse('Nothing to do', status=400)


def citations_cron(request):
    '''
    Citation cron (job) view
    
    :param request: Django request
    '''
    limit = request.GET.get('limit', None)
    asyncresult = tasks.citations_cron.delay(limit=limit)
    task = Task.objects.create(type=Task.TYPE_CITATION_CRON, taskmeta_id=asyncresult.id)
    return JsonResponse(task.as_dict())
