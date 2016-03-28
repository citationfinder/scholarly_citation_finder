#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from requests.exceptions import ConnectionError

from scholarly_citation_finder.apps.core.models import PublicationUrl
from scholarly_citation_finder.tools.crawler.HtmlParser import HtmlParser, HtmlParserUnkownHeaderType
from scholarly_citation_finder.tools.crawler.Duckduckgo import Duckduckgo, DuckduckgoResponseException

logger = logging.getLogger(__name__)


class PublicationDocumentCrawler:
    
    def __init__(self, database='default'):
        self.database = database
        self.html_parser = HtmlParser()
        self.search_engine = Duckduckgo()
        self.publication = None
        self.urls = None
        
    def set(self, publication):
        self.publication = publication
        # Get stored URLs of this publications
        self.urls = PublicationUrl.objects.using(self.database).filter(publication=self.publication)
        logger.info('set publication {}; {} stored urls'.format(publication.id, len(self.urls)))
    
    #def by_stored_pdf_urls(self):
    #    results = []
    #    for url in self.urls.filter(type=PublicationUrl.MIME_TYPE_PDF):
    #        results.append(url.url)
    #    return results
            
    def by_search_engine(self):
        results = []
        if self.publication.title:
            try:
                logger.info('by_search_engine: keywords={}'.format(self.publication.title))
                for result in self.search_engine.query(keywords=self.publication.title, filetype=Duckduckgo.API_PARAM_FILETYPE_PDF, limit=2):
                    if self.__match_title(self.publication.title, result['title_matching']):
                        if result['type'] == Duckduckgo.API_PARAM_FILETYPE_PDF:
                            results.append(result['url'])
                        elif result['type'] is None:
                            results.extend(self.use_html_page_to_find_pdf(result['url']))
                        else:
                            logger.info('unsupported Duckduckgo URL type {}: {}'.format(result['type'], result['url'])) 
            except(DuckduckgoResponseException, ConnectionError) as e:
                logger.warn(e, exc_info=True)
        return results

    def by_soure(self):
        results = []
        source = self.publication.source
        if source:
            if 'citeseerx:' in source:
                results.append('http://citeseerx.ist.psu.edu/viewdoc/download?doi={}&rep=rep1&type=pdf'.format(source.replace('citeseerx:', '')))
            elif 'arxiv:' in source:
                results.append('http://arxiv.org/pdf/{}'.format(source.replace('arxiv:', '')))
        return results

    def by_stored_urls(self):
        results = []
        
        doi_not_in_urls = True
        for url in self.urls:
            if url.type == PublicationUrl.MIME_TYPE_PDF:
                results.append(url.url)
            if url.type in (None, PublicationUrl.MIME_TYPE_HTML):
                if 'dx.doi.org' in url.url:
                    doi_not_in_urls = False
                results.extend(self.use_html_page_to_find_pdf(url.url))
            else:
                logger.info('unsupported URL type {}: {}'.format(url.type, url.url))
        # If the default DOI url was not already in the URLs add it              
        if doi_not_in_urls and self.publication.doi:
            results.extend(self.use_html_page_to_find_pdf('http://dx.doi.org/{}'.format(self.publication.doi)))
        return results       
    
    def use_html_page_to_find_pdf(self, html_url):
        results = []
        try:
            hyperrefs, resolved_url = self.html_parser.find_pdf_hyperrefs(html_url)
            if hyperrefs:
                logger.info('find {} PDF hyperrefs on page: {}'.format(len(hyperrefs), resolved_url))            
                for link in hyperrefs:
                    logger.info('\t{}'.format(link))
                    if link.endswith('.pdf') or link.endswith('/pdf'):
                        results.append(link)
            elif hyperrefs == False:
                results.append(resolved_url)
        except(HtmlParserUnkownHeaderType, ConnectionError) as e:
            logger.warn(e, exc_info=True)
        return results

    """
    def use_search_engine_to_find_pdf(self, title):
        try:
            results = []
            for result in self.search_engine.query(keywords=title, filetype=Duckduckgo.API_PARAM_FILETYPE_PDF, limit=2):
                if self.__match_title(title, result['title_matching']):
                    results.append(result)
                return results
        except(DuckduckgoResponseException, ConnectionError) as e:
            logger.warn(e, exc_info=True)
        return False, None
    """

    def __match_title(self, original_title, found_title_matching, max_num_words_difference=2):
        '''
        
        :param original_title:
        :param found_title_matching:
        '''
        num_words_orignal = len(original_title[:58].split(' '))
        num_words_found = len(found_title_matching.split(' '))
        return abs(num_words_orignal-num_words_found) <= max_num_words_difference
