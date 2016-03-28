#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import json
import csv
from os.path import os

from .PublicationSet import PublicationSet
from scholarly_citation_finder.apps.core.models import PublicationReference
from scholarly_citation_finder.apps.citation.mag.IsiFieldofstudy import IsiFieldofstudy


class EmptyPublicationSetException(Exception):
    pass


class CitationFinder:

    def __init__(self, database='default', evaluation=False):
        self.evaluation = evaluation
        self.database = database
        self.publication_set = PublicationSet(database=self.database)
        self.reset()

    def hack(self):
        # <----- remove
        self.citing_papers = PublicationReference.objects.using(self.database).filter(reference__in=self.publication_set.get())
        
    def reset(self):
        self.publication_set.additional_publications_idstring = ''
        self.citations = []
        self.evaluation_result = []
        
    def run(self, strategies):
        if self.publication_set.is_empty():
            raise EmptyPublicationSetException('publication_search_set is empty')

        self.reset()    
        strategies_name = '+'.join([strategy.name for strategy in strategies])
        
        for strategy in strategies:
            #self.logger.info('run {}'.format(strategy.name))
            strategy.setup(database=self.database)
            strategy.run(self.publication_set, self.inspect_publications)
            
        return strategies_name

    def inspect_publications(self, publications, string=''):
        # <----- remove
        publications_citing = self.citing_papers.filter(publication__in=publications)

        #self.logger.info('{}: found {} publications, {} citations'.format(string, len(publications), len(publications_citing)))
        # add
        for citation in publications_citing:
            if citation not in self.citations:
                self.citations.append(citation)
                self.publication_set.add(citation.publication_id)        
        
        # output for evaluation
        if self.evaluation:
            self.evaluation_result.append([len(publications), len(self.citations)])
        
    def store(self, path, filename, isi_fieldofstudy=False):
        filename = os.path.join(path, '{}.json'.format(filename))
        try:
            results = []
            """
            for publication in self.publication_set.get():
                for citation in self.citations:
                    if citation.reference_id == publication.id:
                        results.append(self.__serialze(publication, self.citations.filter(reference_id=publication.id)))
                        self.citations.remove(citation)
            """
            
            for publication in self.publication_set.get():
                #                                           vvvvvvvvvvvvvvvvvvvvv
                results.append(self.__serialze(publication, self.citations.filter(reference_id=publication.id), isi_fieldofstudy=isi_fieldofstudy))

            with codecs.open(filename, 'w+', encoding='utf-8') as output_file:
                output_file.write(json.dumps(results, indent=4))
                return filename
        except(IOError) as e:
            raise e
    
    def store_evaluation(self, path, filename):
        '''
        
        :param path: File path
        :param filename: File name (without extension)
        :raise IOError: 
        :return: total number of inspected publications, total number of found citations
        '''
        filename = os.path.join(path, '{}.csv'.format(filename))
        try:
            with open(filename, 'w+') as csvfile:
                num_inspected_publications = 0
                writer = csv.writer(csvfile)
                writer.writerow(['num_inspected_publications', 'num_citations'])
                writer.writerow([0, 0])
                if len(self.evaluation_result) > 0:
                    for result in self.evaluation_result:
                        num_inspected_publications += result[0]
                        writer.writerow([num_inspected_publications, result[1]])
                    # return total number of inspected publications and total number of found citations
                    return num_inspected_publications, self.evaluation_result[-1][1]
                else:
                    return 0, 0
        except(IOError) as e:
            raise e

    def __serialze(self, publication, citations=None, isi_fieldofstudy=False):
        
        if self.database == 'mag':
            publication.title = publication.title.title()

        journal_name = None
        if publication.journal_id:
            journal_name = publication.journal.name
            
        if publication.conference_id:
            if publication.conference.name:
                publication.booktitle = publication.conference.name
            else:
                publication.booktitle = publication.conference.short_name
        
        if not publication.type:
            if publication.conference_id:
                publication.type = 'inproceedings'
            if publication.booktitle:
                publication.type = 'incollection'
            else:
                publication.type = 'article'
        
        if publication.volume:
            publication.volume = self.__convert_to_integer(publication.volume)

        if publication.number:
            publication.number = self.__convert_to_integer(publication.number)

        if publication.pages_from:
            publication.pages_from = self.__convert_to_integer(publication.pages_from)

        if publication.pages_to:
            publication.pages_to = self.__convert_to_integer(publication.pages_to)
        
        authors = []
        for item in publication.publicationauthoraffilation_set.all():
            if item.author_id:
                authors.append(item.author.name)
        
        keywords = []        
        for keyword in publication.publicationkeyword_set.all():
            keywords.append(keyword.name)

        result = {'type': publication.type,
                  'title': publication.title,
                  'year': publication.year,
                  'booktitle': publication.booktitle,
                  'journal_name': journal_name,
                  'volumne': publication.volume,
                  'number': publication.number,
                  'pages_from': publication.pages_from,
                  'pages_to': publication.pages_to,
                  'series': publication.series,
                  'publisher': publication.publisher,
                  'isbn': publication.isbn,
                  'doi': publication.doi,
                  'abstract': publication.abstract,
                  'copyright': publication.copyright,
                  'authors': authors,
                  'keywords': keywords,
                  'citations': []}
        
        if isi_fieldofstudy:
            result['isi_fieldofstudy'] = self.__isi_fieldofstudy_mapping(publication)

        if citations:
            for citation in citations:
                result['citations'].append(self.__serialze(citation.publication))
        
        return result
    
    def __convert_to_integer(self, value):
        try:
            return int(value)
        except(ValueError):
            return None
        
    def __isi_fieldofstudy_mapping(self, publication):
        # Sort field of study in descending level order, i.e. check first level 1 and then level 0.
        # Don't consider field of studies with a confidence lower then 0.5
        query = publication.publicationfieldofstudy__set().filter(level__gte=0, level__lte=1).order_by('-level', '-confidence')
        # Iterate over all level 1 and 0 field of studies
        for fieldofstudy in query.iterate():
            if fieldofstudy.level == 0 and fieldofstudy.name in IsiFieldofstudy.mappingLevel0:
                return IsiFieldofstudy.mappingLevel0[fieldofstudy.name]
            elif fieldofstudy.level == 1 and fieldofstudy.name in IsiFieldofstudy.mappingLevel1:
                return IsiFieldofstudy.mappingLevel1[fieldofstudy.name]
        return None
