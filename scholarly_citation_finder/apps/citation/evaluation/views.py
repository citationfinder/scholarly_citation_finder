#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

import tasks
from scholarly_citation_finder.apps.tasks.models import Task
from scholarly_citation_finder import config
from ..strategy.AuthorStrategy import AuthorStrategy
from ..strategy.ConferenceStrategy import ConferenceStrategy
from ..strategy.FieldofstudyStrategy import FieldofstudyStrategy
from ..strategy.JournalStrategy import JournalStrategy
from django.views.decorators.csrf import csrf_exempt

def create(request, name):
    setsize = request.GET.get('setsize', None)
    num_min_publications = request.GET.get('num_min_publications', 0)
    if setsize:
        asyncresult = tasks.evaluation_create_author_set.delay(name=name, setsize=int(setsize), num_min_publications=int(num_min_publications))
        task = Task.objects.create(type=Task.TYPE_EVALUATION_SET, taskmeta_id=asyncresult.id)
        return JsonResponse(task.as_dict())
    else:
        return HttpResponse('Nothing to do', status=400)

    
def create_detail(request, id):
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


@csrf_exempt
def run(request, name):
    if request.body and os.path.isdir(os.path.join(config.EVALUATION_DIR, name)):
        try:
            strategies = eval(request.body)
            
            asyncresult = tasks.evaluation_run.delay(name=name, strategies=strategies)
            task = Task.objects.create(type=Task.TYPE_EVALUATION_RUN, taskmeta_id=asyncresult.id)
            return JsonResponse(task.as_dict())
        except(AttributeError, SyntaxError, TypeError) as e:
            return HttpResponse('Strategies string is not valid. {}: {}'.format(type(e).__name__, str(e)), status=400)
    else:
        return HttpResponse('Nothing to do', status=400)
