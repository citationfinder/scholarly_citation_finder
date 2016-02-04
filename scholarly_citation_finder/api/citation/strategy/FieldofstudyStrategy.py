#!/usr/bin/python
# -*- coding: utf-8 -*-
from ..CitationFinder import CitationFinder
from scholarly_citation_finder.apps.core.models import Publication, PublicationReference, FieldOfStudy

class FieldofstudyStrategy(CitationFinder):


    def __init__(self):
        super(FieldofstudyStrategy, self).__init__(name='fieldofstudy_strategy')
        
    def run(self, publication_limit=None, time_limit=None):
        CitationFinder.run(self, publication_limit=publication_limit, time_limit=time_limit)

        citing_papers = PublicationReference.objects.using(self.database_name).filter(reference__in=self.publication_search_set)
        
    
        fieldofstudies = self.publication_set.get_fieldofstudies()
        self.logger.info('found {} field of studies in search set'.format(len(fieldofstudies)))
        for fieldofstudy in fieldofstudies:
            fieldofstudy_publications = self.__find_fieldofstudy_publications(fieldofstudy.id)            
            fieldofstudy_publications_citing = citing_papers.filter(publication__in=fieldofstudy_publications)
            self.logger.info('field of study "{}": found {} publications, {} citations'.format(fieldofstudy, len(fieldofstudy_publications), len(fieldofstudy_publications_citing)))
            
            for publicationReference in fieldofstudy_publications_citing:
                if publicationReference not in self.publicationreferences_result_set:
                    self.publicationreferences_result_set.append(publicationReference)
            self.output.write_values(len(fieldofstudy_publications), len(self.publicationreferences_result_set))
        self.run_done()
        
    def __find_fieldofstudy_publications(self, fieldofstudy_id):
        return Publication.objects.using(self.database_name).raw('SELECT publication_id AS id from core_publicationkeyword WHERE fieldofstudy_id=%s', [fieldofstudy_id])
        #return Publication.objects.using(self.database_name).filter(publicationkeyword__fieldofstudy_id=fieldofstudy_id)
