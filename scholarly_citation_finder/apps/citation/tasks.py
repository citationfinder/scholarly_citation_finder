#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import shared_task
import os.path
import logging
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .CitationFinder import CitationFinder, EmptyPublicationSetException
from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import create_dir
from scholarly_citation_finder.apps.core.models import Publication
from scholarly_citation_finder.apps.citation.search.CitationExtractor import CitationExtractor

logger = logging.getLogger(__name__)


@shared_task
def citations_find(strategy, type, id=None, name=None, database='default'):
    '''

    :param strategy:    
    :param type:
    :param id:
    :param name:
    :return: Name of the output file
    :raise ObjectDoesNotExits:
    :raise MultipleObjectsReturned:
    :raise EmptyPublicationSetException: 
    :raise Exception: When type is unknown
    '''
    try:
        citationfinder = CitationFinder(database=database)
        if type == 'author':
            id, length_publication_set = citationfinder.publication_set.set_by_author(name=name, id=id)
        elif type == 'conference':
            id, length_publication_set = citationfinder.publication_set.set_by_conference(name=name, id=id)
        elif type == 'journal':
            id, length_publication_set = citationfinder.publication_set.set_by_journal(name=name, id=id)
        else:
            raise Exception('Unknown type: {}'.format(type))
        logger.info('{} {}: set {} publications'.format(id, type, length_publication_set))
        
        strategies_name = citationfinder.run(strategy)
        logger.info('{}: finished strategy "{}"'.format(id, strategies_name))
        
        output_filename = citationfinder.store(path=create_dir(os.path.join(config.DOWNLOAD_TMP_DIR, strategies_name)),
                                               filename=id)
        return output_filename
    except(ObjectDoesNotExist, MultipleObjectsReturned, EmptyPublicationSetException) as e:
        raise e

@shared_task
def citations_cron(limit=None, database='default'):
    try:
        limit = int(limit)
    except(ValueError):
        limit = None
    
    query = Publication.objects.using(database).filter(source_extracted__isnull=True)
    if limit:
        query = query[:limit]

    citationextractor = CitationExtractor(database=database)
    citationextractor.run(query)
