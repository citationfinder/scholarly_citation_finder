#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from scholarly_citation_finder import config
from scholarly_citation_finder.apps.parser.PublicationPdfCrawler import PublicationPdfCrawler
from scholarly_citation_finder.apps.core.models import Publication, PublicationUrl
from scholarly_citation_finder.tools.extractor.grobid.GrobidExtractor import GrobidExtractor,\
    GrobidServceNotAvaibleException
from scholarly_citation_finder.lib.file import download_file_pdf, DownloadPdfException
from scholarly_citation_finder.apps.parser.Parser import Parser
from scholarly_citation_finder.lib.process import ProcessException
from scholarly_citation_finder.tools.extractor.grobid.TeiParser import TeiParserNoDocumentTitle,\
    TeiParserNoReferences
from scholarly_citation_finder.apps.parser.Exceptions import ParserRollbackError

logger = logging.getLogger(__name__)


class CitationFinder2:

    NUM_MINIMUM_REFERENCES = 3

    def __init__(self, database='default'):
        self.database = database
        self.publicationpdf_crawler = PublicationPdfCrawler(database=self.database)
        self.extractor = GrobidExtractor()
        self.parser = Parser(database=database)
    
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
        logger.info('find citations for publication {} ----------------------'.format(publication.id))
        self.publicationpdf_crawler.set(publication)
            
        #self.publicationpdf_crawler.pdf_by_stored_pdf_urls()
        #self.publicationpdf_crawler.pdf_by_soure()

        urls = self.publicationpdf_crawler.by_stored_urls()
        if self.extract_documents(publication, urls):
            return True

        #urls = self.publicationpdf_crawler.by_search_engine()
        #if self.extract_pdfs(publication, urls):
        #    return True

        return False
        
    def extract_documents(self, publication, pdfs_as_urls):
        logger.info('extract_pdfs: {}'.format(len(pdfs_as_urls)))
        for url in pdfs_as_urls:
            logger.warn('\t{}'.format(url))
        
            try:
                document_meta, references = self.__extract_document(publication.title, publication.id, url=url)
                if document_meta and references:
                    self.__store_document_meta(publication=publication, document_meta=document_meta)
                    self.__store_references(publication=publication, url=url, references=references)
                    return True
            except(ProcessException, GrobidServceNotAvaibleException) as e:
                logger.info('{}: {}'.format(type(e).__name__, str(e)))
            except(ParserRollbackError) as e:
                logger.warn(e, exc_info=True)
        return False

    def __extract_document(self, publication_title, publication_id, url):
        '''
        Try to download the document from the given URL and extract it
        
        :param publication_title: Title of the publication to check, if it's the correct document
        :param publication_id: ID of the publication. Used for the filename of the temporary stored document
        :param url: Document URL
        :return: Document meta object, references array
                 False, False if (a) it failed to download the document (b) or the document has no title or references
        :raise ProcessException: Grobid failed
        :raise GrobidServceNotAvaibleException: Grobid is not available
        '''
        try:
            filename = download_file_pdf(url, path=config.DOWNLOAD_TMP_DIR, name='{}_tmp.pdf'.format(publication_id))
            document_meta, references = self.extractor.extract_file(filename, completely=True)
            
            # Check title
            document_meta['title'] = document_meta['title'].lower().strip()
            if document_meta['title'] != publication_title:
                logger.info('Wrong title! Is "%s", should "%s"' % (document_meta['title'], publication_title) )
                return False, False
            
            # Check number of references
            if len(references) < self.NUM_MINIMUM_REFERENCES:
                logger.info('Not enough references')
                return False, False
            
            return document_meta, references
                
        # Invalid document
        except(DownloadPdfException, TeiParserNoDocumentTitle, TeiParserNoReferences) as e:
            logger.info('{}: {}'.format(type(e).__name__, str(e)))
            return False, False
        # Extractor failed
        except(ProcessException, GrobidServceNotAvaibleException) as e:
            raise e
        
    def __store_references(self, publication, references, url):
        '''
        Store the URL and the references
        
        :param publication: Publication object
        :param url: URL
        :param references: References list
        :raise ParserRollbackError: Storage of the references failed
        '''
        publication_url = publication.publicationurl_set.create(url=url,
                                                                type=PublicationUrl.MIME_TYPE_PDF,
                                                                extraction_date=datetime.now())
        for reference in references:
            # TODO: check if paper already exists (!)
            reference['reference']['publication_id'] = publication.id
            reference['reference']['source_id'] = publication_url.id
            reference['publication']['source'] = '{}:{}'.format(reference['publication']['source'], publication_url.id)
            self.parser.parse(**reference)

        try:
            self.parser.commit()
        except(ParserRollbackError) as e:
            raise e
        
    def __store_document_meta(self, publication, document_meta):        
        if 'keywords' in document_meta:
            for keyword in document_meta['keywords']:
                publication.publicationkeyword_set.get_or_create(name=keyword)
