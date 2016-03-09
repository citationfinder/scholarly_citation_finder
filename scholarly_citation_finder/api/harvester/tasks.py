from __future__ import absolute_import
from celery import shared_task
import logging

from scholarly_citation_finder.api.harvester.OaiHarvester import OaiHarvester
from scholarly_citation_finder.api.harvester.dblp.DblpHarvester import DblpHarvester

logger = logging.getLogger(__name__)


@shared_task
def oaipmh_harvest(name, oai_url, oai_identifier, **kwargs):
    harvester = OaiHarvester(name=name, oai_url=oai_url, oai_identifier=oai_identifier)
    return harvester.harvest(**kwargs)


@shared_task
def dblp_harevester(**kwargs):
    harvester = DblpHarvester()
    return harvester.harvest(**kwargs)