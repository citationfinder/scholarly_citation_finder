#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from scholarly_citation_finder.apps.core.models import Publication
from scholarly_citation_finder.api.citation.strategy.Strategy import Strategy

logger = logging.getLogger(__name__)


class FieldofstudyStrategy(Strategy):


    def __init__(self, ordered=False, limit=None):
        name = 'fieldofstudy'
        if ordered:
            name += '-ordered'
        if limit > 0:
            name += '-limit'
        super(FieldofstudyStrategy, self).__init__(name=name)
        self.ordered = ordered
        self.limit = limit
        
    def run(self, publication_set, callback):
        fieldofstudies = publication_set.get_fieldofstudies(self.ordered)
        if self.limit > 0:
            fieldofstudies = fieldofstudies[:self.limit]
        logger.info('found {} (limit: {}) field of studies in search set'.format(len(fieldofstudies), self.limit))
        fieldofstudies_publications = self.__find_fieldofstudies_publications(fieldofstudies, publication_set.get_min_year())
        callback(fieldofstudies_publications, 'field of studies')
        #for fieldofstudy in fieldofstudies:
        #    fieldofstudy_publications = self.__find_fieldofstudy_publications(fieldofstudy.id, publication_set.get_min_year())
        #    fieldofstudy_publications_citing = citing_papers.filter(publication__in=fieldofstudy_publications)
        #    logger.info('field of study "{}": found {} publications (year >= {}), {} citations'.format(fieldofstudy, len(fieldofstudy_publications), publication_set.get_min_year(), len(fieldofstudy_publications_citing)))  
        #    citation_set.add(fieldofstudy_publications_citing, len(fieldofstudy_publications))

    def __find_fieldofstudies_publications(self, fieldofstudies, min_year):
        return Publication.objects.using(self.database).filter(publicationkeyword__fieldofstudy__in=fieldofstudies).filter(year__gte=min_year).distinct()

        
    #def __find_fieldofstudy_publications(self, fieldofstudy_id, min_year):
        #return list(Publication.objects.using(self.database).raw("SELECT DISTINCT publication_id AS id from core_publicationkeyword WHERE fieldofstudy_id=%s", [fieldofstudy_id]))
    #    return Publication.objects.using(self.database).filter(publicationkeyword__fieldofstudy_id=fieldofstudy_id).filter(year__gte=min_year).distinct()
