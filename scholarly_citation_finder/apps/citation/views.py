#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

import tasks
from scholarly_citation_finder.apps.tasks.models import Task
from scholarly_citation_finder import config
from .strategy.AuthorStrategy import AuthorStrategy
from .strategy.ConferenceStrategy import ConferenceStrategy
from .strategy.FieldofstudyStrategy import FieldofstudyStrategy
from .strategy.JournalStrategy import JournalStrategy


def citations_find(request):
    type = request.GET.get('type', None)
    name = request.GET.get('name', None)
    id = request.GET.get('id', None)
    if type in ('author', 'conference', 'journal') and (name or id) and request.body:
        try:
            asyncresult = tasks.citations_find.delay(type=type,
                                                     name=name,
                                                     id=int(id),
                                                     strategy=eval(request.body))
            task = Task.objects.create(type=Task.TYPE_CITATION_FIND, taskmeta_id=asyncresult.id)
            return JsonResponse(task.as_dict())
        except(AttributeError, SyntaxError, TypeError) as e:
            return HttpResponse('Strategies string is not valid. {}: {}'.format(type(e).__name__, str(e)), status=400)
    else:
        return HttpResponse('Nothing to do', status=400)


def citations_cron(request):
    limit = request.GET.get('limit', None)
    asyncresult = tasks.citations_cron.delay(limit=limit)
    return HttpResponse('started task')   
