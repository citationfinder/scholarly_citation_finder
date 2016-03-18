#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from scholarly_citation_finder import config
from scholarly_citation_finder.apps.parser import PublicationPdfCrawler
from scholarly_citation_finder.apps.core.models import Publication, PublicationUrl
from scholarly_citation_finder.tools.extractor.grobid.GrobidExtractor import GrobidExtractor,\
    GrobidServceNotAvaibleException
from scholarly_citation_finder.lib.file import download_file_pdf, DownloadPdfException
from scholarly_citation_finder.apps.parser.Parser import Parser
from scholarly_citation_finder.lib.process import ProcessException

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
        if self.extract_pdfs(publication, urls):
            return True

        #urls = self.publicationpdf_crawler.by_search_engine()
        #if self.extract_pdfs(publication, urls):
        #    return True

        return False
        
    def extract_pdfs(self, publication, pdfs_as_urls):
        logger.info('extract_pdfs: {}'.format(len(pdfs_as_urls)))
        for url in pdfs_as_urls:
            logger.warn('\t{}'.format(url))
        
            try:
                filename = download_file_pdf(url, path=config.DOWNLOAD_TMP_DIR, name='{}_tmp.pdf'.format(publication.id))
                extraction_result = self.__extract_pdf(publication, filename=filename, url=url)
                if extraction_result:
                    return extraction_result
            except(DownloadPdfException, GrobidServceNotAvaibleException) as e:
                logger.info('{}: {}'.format(type(e).__name__, str(e)))
        return False

    def __extract_pdf(self, publication, filename, url):
        try:
            references = self.extractor.extract_file(filename)
            # TODO: maybe check title
            if len(references) >= self.NUM_MINIMUM_REFERENCES:
                publication_url = publication.publicationurl_set.create(url=url,
                                                                        type=PublicationUrl.MIME_TYPE_PDF,
                                                                        extraction_date=datetime.now())
                        
                for reference in references:
                    # TODO: check if paper already exists (!)
                    reference['reference']['publication_id'] = publication.id
                    reference['reference']['source_id'] = publication_url.id
                    reference['publication']['source'] = '{}:{}'.format(reference['publication']['source'], publication_url.id)
                    self.parser.parse(**reference)
                self.parser.commit()
                return True
            else:
                return False
        except(ProcessException) as e:
            logger.warn(e, exc_info=True)
        except(GrobidServceNotAvaibleException) as e:
            raise e