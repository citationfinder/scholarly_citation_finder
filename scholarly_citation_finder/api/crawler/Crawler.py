from scholarly_citation_finder.apps.core.models import Publication,\
    PublicationUrl
import logging
from django.core.exceptions import ObjectDoesNotExist
from scholarly_citation_finder.api.crawler.PdfFinder import PdfFinder

logger = logging.getLogger(__name__)

class Crawler:
    
    database = None
    pdfFinder = None
    
    def __init__(self):
        self.database = 'mag'
        self.pdfFinder = PdfFinder()
    
    def run(self, publication):
        if publication.source_extracted:
            logger.info('publication {} already extracted'.format(publication.id))
            return
            
        # 1. Get stored URLs of this publications
        urls = PublicationUrl.objects.using(self.database).filter(publication=publication)
            
        # 1.1 First check URLs of type PDF
        for url in urls.filter(type=PublicationUrl.MIME_TYPE_PDF):
            logger.info('PDF: {}'.format(url.url))

        # 1.2 Check URLs with oter types
        for url in urls:
            if url.type in (None, PublicationUrl.MIME_TYPE_HTML):
                logger.info('{}'.format(url.url))
            #self.pdfFinder.find_pdf(url.url)
                # if that was successful, replace current URL with that one
                # for unsupported type, store that type?
            #else:
            #    logger.info('unsupported format {}: {}'.format(url.type, url.url))
            return
        
        # 1.3
        # Check source, if CiteSeerX download it from there
        # Check DOI(!)
        
        # 1.4
        # search for pdf
            
    
    def run_by_id(self, publication_id):
        try:
            return self.run(Publication.objects.using(self.database).get(pk=publication_id))
        except(ObjectDoesNotExist):
            return False
        
    def extract_pdf(self, publication, url):
        pass
    
    