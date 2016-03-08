import logging

from scholarly_citation_finder.api.crawler import PdfCrawler
from scholarly_citation_finder.apps.core.models import Publication

logger = logging.getLogger(__name__)


class CitationFinder:
    
    def __init__(self, database='default'):
        self.database = database
        self.publication_crawler = PdfCrawler(database=self.database)
    
    def run(self):
        for publication in Publication.objects.using(self.database).exclude(source_extracted__isnull=True):
            self.find_citations(publication)

    def find_citations(self, publication):
        self.publication_crawler.set(publication)
            
        #self.publication_crawler.pdf_by_stored_pdf_urls()
        #self.publication_crawler.pdf_by_soure()
        urls = self.publication_crawler.by_stored_other_urls()
        if self.extract_pdf(urls):
            break
        urls = self.publication_crawler.by_search_engine()
        if self.extract_pdf(urls):
            break
        
    def extract_pdf(self, pdfs_as_urls):
        for url in pdfs_as_urls:
            logger.warn(url)
            # TODO: call Grobid
        return False
