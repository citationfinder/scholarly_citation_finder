#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from requests.exceptions import ConnectionError, Timeout

from scholarly_citation_finder.apps.core.models import PublicationUrl
from scholarly_citation_finder.tools.crawler.HtmlParser import HtmlParser, HtmlParserUnkownHeaderType
from scholarly_citation_finder.tools.crawler.engine.Duckduckgo import Duckduckgo
from scholarly_citation_finder.tools.nameparser.StringMatching import words_difference, nearly_match
from scholarly_citation_finder.tools.crawler.engine.SearchEngine import SearchEngineResponseException
from scholarly_citation_finder.tools.crawler.engine.Bing import Bing

logger = logging.getLogger(__name__)


class PublicationDocumentCrawler:
    '''
    Class to find a document of a publication.
    '''
    
    def __init__(self, database='default'):
        '''
        Create object.
        
        :param database: Database name
        '''
        self.database = database
        self.html_parser = HtmlParser()
        self.search_engine = Duckduckgo()
        self.publication = None

    def set(self, publication):
        '''
        Set the publication.
        
        :param publication: Publication object
        '''
        self.publication = publication
        #logger.info('set publication {}'.format(publication.id))
    
    #def get_by_stored_pdf_urls(self):
    #    results = []
    #    for url in self.urls.filter(type=PublicationUrl.MIME_TYPE_PDF):
    #        results.append(url.url)
    #    return results
            
    def get_by_search_engine(self, keywords=None):
        '''
        Get the document by search engine.
        
        :param keywords: Query keyword string
        :return: List of URLs, which refer to documents
        '''
        results = []
        keywords = keywords if keywords else self.publication.title
        if keywords:
            logger.info('get_by_search_engine: keywords=%s' % keywords)
            try:
                for result in self.search_engine.query(keywords=keywords, filetype=self.search_engine.API_PARAM_FILETYPE_PDF, limit=2):
                    #if words_difference(keywords[:self.search_engine.TITLE_LENGTH], result['title_matching']):
                    if self.search_engine.nearly_match_titles(keywords, result['title']):
                        if result['type'] == self.search_engine.API_PARAM_FILETYPE_PDF:
                            results.append(result['url'])
                        elif result['type'] is None:
                            results.extend(self.__find_document_on_website(result['url']))
                        else:
                            logger.info('Unsupported URL type {}: {}'.format(result['type'], result['url']))
                    #else:
                    #    logger.info('"%s" and "%s" does not match' % (keywords, result['title_matching']))
            except(SearchEngineResponseException, Timeout, ConnectionError) as e:
                logger.warn(str(e))
                self.search_engine = Bing()
        return results

    def get_by_soure(self):
        '''
        Get the document by the stored source.
        '''
        results = []
        source = self.publication.source
        if source:
            if 'citeseerx:' in source:
                results.append('http://citeseerx.ist.psu.edu/viewdoc/download?doi={}&rep=rep1&type=pdf'.format(source.replace('citeseerx:', '')))
            elif 'arxiv:' in source:
                results.append('http://arxiv.org/pdf/{}'.format(source.replace('arxiv:', '')))
        return results

    def get_by_stored_urls(self):
        '''
        Get the document by the stored URLs.
        '''
        results = []
        
        doi_not_in_urls = True
        for url in PublicationUrl.objects.using(self.database).filter(publication=self.publication):
            if url.type == PublicationUrl.MIME_TYPE_PDF:
                results.append(url.url)
            if url.type in (None, PublicationUrl.MIME_TYPE_HTML):
                if 'dx.doi.org' in url.url:
                    doi_not_in_urls = False
                results.extend(self.__find_document_on_website(url.url))
            else:
                logger.info('unsupported URL type {}: {}'.format(url.type, url.url))
        # If the default DOI URL was not already in the URLs add it              
        if doi_not_in_urls and self.publication.doi:
            results.extend(self.__find_document_on_website('http://dx.doi.org/{}'.format(self.publication.doi)))
        return results       
    
    def __find_document_on_website(self, html_url):
        '''
        Find documents on a website.
        
        :param html_url: HTML code of a website
        '''
        results = []
        try:
            hyperrefs, resolved_url = self.html_parser.find_pdf_hyperrefs(html_url)
            if hyperrefs:
                logger.info('find %s PDF hyperrefs on page: %s' % (len(hyperrefs), resolved_url))            
                for link in hyperrefs:
                    logger.info('\t{}'.format(link))
                    if link.endswith('.pdf') or link.endswith('/pdf'):
                        results.append(link)
            elif hyperrefs == False:
                results.append(resolved_url)
        except(HtmlParserUnkownHeaderType, ConnectionError) as e:
            logger.warn(str(e))
        return results
