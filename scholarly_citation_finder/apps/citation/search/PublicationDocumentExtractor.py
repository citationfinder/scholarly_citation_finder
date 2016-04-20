#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from scholarly_citation_finder import config
from scholarly_citation_finder.apps.parser.Parser import Parser
from scholarly_citation_finder.apps.core.models import PublicationUrl
from scholarly_citation_finder.tools.extractor.grobid.GrobidExtractor import GrobidExtractor,\
    GrobidServceNotAvaibleException
from scholarly_citation_finder.lib.file import download_file_pdf, DownloadFailedException, UnexpectedContentTypeException
from scholarly_citation_finder.lib.process import ProcessException
from scholarly_citation_finder.apps.parser.Exceptions import ParserRollbackError
from scholarly_citation_finder.lib.string import normalize_string
from scholarly_citation_finder.tools.extractor.grobid.TeiParser import TeiParserNoDocumentTitle,\
    TeiParserNoReferences
from scholarly_citation_finder.tools.nameparser.StringMatching import nearly_match

logger = logging.getLogger(__name__)


class PublicationDocumentExtractor:
    
    NUM_MINIMUM_REFERENCES = 3

    def __init__(self, database='default'):
        self.extractor = GrobidExtractor() # used to extract documents
        self.parser = Parser(database=database) # used to store results
      
    def extract_and_store(self, publication, url):
        try:
            document_meta, references = self.extract(publication.title, publication.id, url=url)
            if document_meta and references:
                self.__store_document_meta(publication=publication, document_meta=document_meta)
                self.__store_references(publication=publication, url=url, references=references)
                return True
        # Download failed
        except(DownloadFailedException, UnexpectedContentTypeException) as e:
            logger.info('{}: {}'.format(type(e).__name__, str(e)))
        # Extractor failed
        except(ProcessException, GrobidServceNotAvaibleException) as e:
            logger.info('{}: {}'.format(type(e).__name__, str(e)))
        # Storage failed
        except(ParserRollbackError) as e:
            logger.warn(e, exc_info=True)
        return False

    def extract(self, publication_title, publication_id, url):
        '''
        Try to download the document from the given URL and extract it
        
        :param publication_title: Title of the publication to check, if it's the correct document
        :param publication_id: ID of the publication. Used for the filename of the temporary stored document
        :param url: Document URL
        :return: Document meta object, references array
                 False, False if (a) it failed to download the document (b) or the document has no title or references
        :raise ProcessException: Extractor failed
        :raise GrobidServceNotAvaibleException: Extractor is not available
        :raise DownloadFailedException: Download failed
        :raise UnexpectedContentTypeException: File for given URL has the wrong content type
        '''
        try:
            filename = download_file_pdf(url, path=config.DOWNLOAD_TMP_DIR, name='{}_tmp.pdf'.format(publication_id))
            document_meta, references = self.extractor.extract_file(filename, completely=True)
            
            # Check title
            document_meta_title = document_meta['publication']['title'].lower().strip()
            if not nearly_match(document_meta_title, publication_title):
                logger.info('Wrong title! Is "%s", should "%s"' % (document_meta_title, publication_title) )
                return False, False
            
            # Check number of references
            if len(references) < self.NUM_MINIMUM_REFERENCES:
                logger.info('Not enough references')
                return False, False
            
            return document_meta, references

        # Tei failed (invalid document)
        except(TeiParserNoDocumentTitle, TeiParserNoReferences) as e:
            logger.info('{}: {}'.format(type(e).__name__, str(e)))
            return False, False

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
                keyword = normalize_string(keyword)
                publication.publicationkeyword_set.get_or_create(name=keyword)