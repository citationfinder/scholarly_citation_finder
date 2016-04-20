#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from .PublicationDocumentExtractor import PublicationDocumentExtractor
from .PublicationDocumentCrawler import PublicationDocumentCrawler

logger = logging.getLogger(__name__)


class CitationExtractor:
    
    def __init__(self, database='default'):
        self.database = database
        self.document_crawler = PublicationDocumentCrawler(database=database)
        self.document_extractor = PublicationDocumentExtractor(database=database)

    def run(self, publications):
        '''
        
        :param publications: List of publication objects
        #:return: List of successful extracted publications 
        '''
        #extracted_publication = []
        
        for publication in publications:
            # If publication was not already extracted
            if not publication.source_extracted:
                publication.source_extracted = self.find_citations(publication)
                logger.info(publication.source_extracted)
                publication.save()
                #if publication.source_extracted:
                #    extracted_publication.append(publication)
                
        #return extracted_publication

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
        if urls and self.extract_document_from_urls(publication, urls):
            return True

        #urls = self.document_crawler.get_by_search_engine()
        #if urls and self.extract_document_from_urls(publication, urls):
        #    return True

        return False

    def extract_document_from_urls(self, publication, pdfs_as_urls):
        logger.info('extract_pdfs: {}'.format(len(pdfs_as_urls)))
        for url in pdfs_as_urls:
            logger.warn('\t{}'.format(url))
            result = self.document_extractor.extract_and_store(publication, url)
            if result:
                return True
        return False
