#!/usr/bin/python
# -*- coding: utf-8 -*-
from scholarly_citation_finder.apps.core.models import Publication, PublicationReference
from scholarly_citation_finder.api.citation.strategy.Strategy import Strategy

class FieldofstudyStrategy(Strategy):


    def __init__(self, ordered=False):
        name = 'fieldofstudy'
        if ordered:
            name += '-ordered'
        super(FieldofstudyStrategy, self).__init__(name=name)
        self.ordered = ordered
        
    def run(self, publication_set, citation_set):
        citing_papers = PublicationReference.objects.using(self.database).filter(reference__in=publication_set.get())
        
    
        fieldofstudies = publication_set.get_fieldofstudies(self.ordered)
        self.logger.info('found {} field of studies in search set'.format(len(fieldofstudies)))
        for fieldofstudy in fieldofstudies:
            fieldofstudy_publications = self.__find_fieldofstudy_publications(fieldofstudy.id)            
            fieldofstudy_publications_citing = citing_papers.filter(publication__in=fieldofstudy_publications)
            self.logger.info('field of study "{}": found {} publications, {} citations'.format(fieldofstudy, len(fieldofstudy_publications), len(fieldofstudy_publications_citing)))
            
            citation_set.add(fieldofstudy_publications_citing, len(fieldofstudy_publications))
        
    def __find_fieldofstudy_publications(self, fieldofstudy_id):
        return list(Publication.objects.using(self.database).raw('SELECT DISTINCT publication_id AS id from core_publicationkeyword WHERE fieldofstudy_id=%s', [fieldofstudy_id]))
        #return Publication.objects.using(self.database).filter(publicationkeyword__fieldofstudy_id=fieldofstudy_id)
