import logging

from scholarly_citation_finder import config
from scholarly_citation_finder.api.crawler import PublicationPdfCrawler
from scholarly_citation_finder.apps.core.models import Publication
from scholarly_citation_finder.api.extractor.grobid.GrobidExtractor import GrobidExtractor
from scholarly_citation_finder.lib.file import download_file_pdf,\
    DownloadPdfException
from scholarly_citation_finder.api import Parser

logger = logging.getLogger(__name__)


class CitationFinder2:
    
    def __init__(self, database='default'):
        self.database = database
        self.publicationpdf_crawler = PublicationPdfCrawler(database=self.database)
        self.extractor = GrobidExtractor()
        self.parser = Parser(database=database)
    
    def run(self):
        for publication in Publication.objects.using(self.database).exclude(source_extracted__isnull=True):
            self.find_citations(publication)

    def find_citations(self, publication):
        self.publicationpdf_crawler.set(publication)
            
        #self.publicationpdf_crawler.pdf_by_stored_pdf_urls()
        #self.publicationpdf_crawler.pdf_by_soure()
        urls = self.publicationpdf_crawler.by_stored_other_urls()
        if self.extract_pdfs(publication, urls):
            break
        urls = self.publicationpdf_crawler.by_search_engine()
        if self.extract_pdfs(publication, urls):
            break
        
    def extract_pdfs(self, publication, pdfs_as_urls):
        for url in pdfs_as_urls:
            logger.warn(url)
            continue # <-- debug only
        
            try:
                filename = download_file_pdf(url, path=url, path=config.DOWNLOAD_TMP_DIR, name='tmp.pdf')
                references = self.extractor.extract_file(filename)
                for reference in references:
                    reference['reference']['publication_id'] = publication.id
                    self.parser.parse(**reference)
            except(DownloadPdfException) as e:
                logger.info(e, exc_info=True)
        return False
