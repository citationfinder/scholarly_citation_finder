#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from .search.PublicationDocumentCrawler import PublicationDocumentCrawler
from scholarly_citation_finder.apps.core.models import Publication
from scholarly_citation_finder.lib.django import queryset_iterator
from .search.PublicationDocumentExtractor import PublicationDocumentExtractor

logger = logging.getLogger(__name__)


class CitationFinder2:

    def __init__(self, database='default'):
        self.database = database
        self.document_crawler = PublicationDocumentCrawler(database=database)
        self.document_extractor = PublicationDocumentExtractor(database=database)
    
    def run(self, limit=None):
        try:
            limit = int(limit)
        except(ValueError):
            limit = None

        query = Publication.objects.using(self.database).filter(source_extracted__isnull=True)
        if limit:
            query = query[:limit]

        for publication in query:
            publication.source_extracted = self.find_citations(publication)
            logger.info(publication.source_extracted)
            publication.save()

    def find_citations(self, publication):
        '''
        :param publication: 
        :return: Boolean True, if citations were found
        '''
        logger.info('find references of publication {} ----------------------'.format(publication.id))
        self.document_crawler.set(publication)
            
        # stored citations

        #self.document_crawler.pdf_by_stored_pdf_urls()
        #self.document_crawler.pdf_by_soure()

        urls = self.document_crawler.get_by_stored_urls()
        if urls and self.extract_documents(publication, urls):
            return True

        #urls = self.document_crawler.get_by_search_engine()
        #if urls and self.extract_documents(publication, urls):
        #    return True

        return False
        
    def extract_documents(self, publication, pdfs_as_urls):
        logger.info('extract_pdfs: {}'.format(len(pdfs_as_urls)))
        for url in pdfs_as_urls:
            logger.warn('\t{}'.format(url))
            result = self.document_extractor.extract_and_store(publication, url)
            if result:
                return True
        return False
