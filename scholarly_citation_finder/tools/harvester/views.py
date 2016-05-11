#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from scholarly_citation_finder.apps.tasks.models import Task
from scholarly_citation_finder.tools.harvester import tasks
from scholarly_citation_finder.tools.harvester.models import Harvester

def oaipmh(request, name):
    '''
    View of OAI-PMH harvester.
    
    :param request: Django request
    :param name: Name of the harvester
    :return: Created task or error code
    '''
    try:
        oaipmh_provider = Harvester.objects.filter(type=Harvester.TYPE_OAI).get(name=name)            
        harvest_parameter = {'limit': request.GET.get('limit', None), 
                             '_from': request.GET.get('from', None),
                             'until': request.GET.get('until', None),
                             'resumptionToken': request.GET.get('resumptiontoken', None)}
        asyncresult = tasks.oaipmh_harvest.delay(name=oaipmh_provider.name,
                                                 oai_url=oaipmh_provider.oai_url,
                                                 oai_identifier=oaipmh_provider.oai_identifier,
                                                 **harvest_parameter)
        task = Task.objects.create(type=Task.TYPE_HARVESTER, taskmeta_id=asyncresult.id)
        return JsonResponse(task.as_dict())
    except(ObjectDoesNotExist) as e:
        return HttpResponse(str(e), status=404)


def dblp(request):
    '''
    View of DBLP harvester.
    
    :param request: Django request
    :return: Created task or error code
    '''
    try:
        harvest_parameter = {'limit': request.GET.get('limit', None), 
                             '_from': request.GET.get('from', None)}
        asyncresult = tasks.dblp_harevester.delay(**harvest_parameter)
        task = Task.objects.create(type=Task.TYPE_HARVESTER, taskmeta_id=asyncresult.id)
        return JsonResponse(task.as_dict())
    except(IOError) as e:
        return HttpResponse(str(e), status=503)
