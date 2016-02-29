#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from scholarly_citation_finder.apps.tasks.models import Task
from scholarly_citation_finder.api.harvester import tasks
from scholarly_citation_finder.api.harvester.models import OaiPmhProvider

def oaipmh(request, name):
    try:
        oaipmh_provider = OaiPmhProvider.objects.get(name=name)            
        harvest_parameter = {'limit': request.GET.get('limit', None), 
                             '_from': request.GET.get('from', None),
                             'until': request.GET.get('until', None),
                             'resumptionToken': request.GET.get('resumptiontoken', None)}
        asyncresult = tasks.oaipmh_harvest.delay(name=oaipmh_provider.name,
                                                 oai_url=oaipmh_provider.url,
                                                 oai_identifier=oaipmh_provider.identifier,
                                                 **harvest_parameter)
        task = Task.objects.create(type=Task.TYPE_HARVESTER, taskmeta_id=asyncresult.id)
        return JsonResponse(task.as_dict())
    except(ObjectDoesNotExist) as e:
        return HttpResponse(str(e), status=404)