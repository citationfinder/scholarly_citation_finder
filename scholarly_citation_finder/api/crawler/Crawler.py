import logging
from django.core.exceptions import ObjectDoesNotExist
from requests.exceptions import ConnectionError

from scholarly_citation_finder.apps.core.models import Publication, PublicationUrl
from scholarly_citation_finder.api.crawler.search.HtmlParser import HtmlParser, HtmlParserUnkownHeaderType
from scholarly_citation_finder.api.crawler.search.Duckduckgo import Duckduckgo, DuckduckgoResponseException


logger = logging.getLogger(__name__)

class Crawler:
    
    database = None
    html_parser = None
    search_engine = None
    
    def __init__(self):
        self.database = 'mag'
        self.html_parser = HtmlParser()
        self.search_engine = Duckduckgo()
    
    def run(self, publication):
        if publication.source_extracted:
            logger.info('publication {} already extracted'.format(publication.id))
            return
        if not publication.title:
            logger.info('publication {} has no title'.format(publication.id))
            return
            
        # 1. Get stored URLs of this publications
        urls = PublicationUrl.objects.using(self.database).filter(publication=publication)
            
        # 1.1 First check URLs of type PDF
        for url in urls.filter(type=PublicationUrl.MIME_TYPE_PDF):
            self.extract_pdf(publication, url.url)
            # --> store result
            # --> in success case stop

        # 1.2
        # search for pdf
        tmp_url, tmp_url_type = self.use_search_engine_to_find_pdf(publication.title)
        if tmp_url:
            if tmp_url_type == Duckduckgo.API_PARAM_FILETYPE_PDF:
                self.extract_pdf(publication, tmp_url)
                # --> in success case: store url
                pass
            elif tmp_url_type is None:
                # --> call use_html_page_to_find_pdf
                pass

        # 1.3 Check URLs with oter types
        if 'citeseerx:' in publication.source:
            self.extract_pdf(publication, url='http://citeseerx.ist.psu.edu/viewdoc/download?doi={}&rep=rep1&type=pdf'.format(publication.source.replace('citeseerx:', '')))
                    
        if publication.doi:
            urls.append(PublicationUrl(url='http://dx.doi.org/{}'.format(publication.doi), type=None))
        for url in urls:
            if url.type in (None, PublicationUrl.MIME_TYPE_HTML):
                logger.info('{}'.format(url.url))
            #self.html_parser.find_pdf(url.url)
                # if that was successful, replace current URL with that one
                # for unsupported type, store that type?
            #else:
            #    logger.info('unsupported format {}: {}'.format(url.type, url.url))

    
    def run_by_id(self, publication_id):
        try:
            return self.run(Publication.objects.using(self.database).get(pk=publication_id))
        except(ObjectDoesNotExist):
            return False
        
    def extract_pdf(self, publication, url):
        logger.info('PDF: {}'.format(url))
        pass

    def use_html_page_to_find_pdf(self, url):
        try:
            hyperrefs = self.html_parser.find_pdf_hyperrefs(url)
            for link in hyperrefs:
                if link.endswith('.pdf') or link.endswith('/pdf'):
                    return link
            return hyperrefs[-1]
            
        except(HtmlParserUnkownHeaderType, ConnectionError) as e:
            logger.warn(e, exc_info=True)
        return False

    def use_search_engine_to_find_pdf(self, title):
        try:
            results = self.search_engine.query(keywords=title, filetype=Duckduckgo.API_PARAM_FILETYPE_PDF, limit=2)
            for result in results:
                if self.__match_title(title, result['title_matching']):
                    return result['url'], result['type']
        except(DuckduckgoResponseException, ConnectionError) as e:
            logger.warn(e, exc_info=True)
        return False, None
    
    def __match_title(self, original_title, found_title_matching, max_num_words_difference=2):
        '''
        
        :param original_title:
        :param found_title_matching:
        '''
        num_words_orignal = len(original_title[:58].split(' '))
        num_words_found = len(found_title_matching.split(' '))
        return abs(num_words_orignal-num_words_found) <= max_num_words_difference
