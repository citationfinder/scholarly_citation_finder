#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup

from .SearchEngine import SearchEngineResponseException
from scholarly_citation_finder.tools.crawler.engine import SearchEngine


class Bing(SearchEngine):
    
    API_URL = 'https://bing.com/search'
    
    API_PARAM_QUERY = 'q'
    API_PARAM_FILETYPE_PDF = 'pdf'

    CSS_RESULT_ELEMENT = 'a'
    CSS_RESULT_ELEMENT_HREF = re.compile('http')
    CSS_RESULT_ELEMENT_MATCHING_KEYWORDS = 'strong'
    #CSS_RESULT_TYPE_ELEMENT = 'span'
    #CSS_RESULT_TYPE_ELEMENT_CLASS = 'result__type'
    
    TITLE_LENGTH = 52

    def query(self, keywords, filetype=None, limit=None):
        '''
        @see parent method
        '''
        keywords = keywords.strip()
        if filetype:
            keywords = 'filetype:%s %s' % (filetype, keywords)
        
        r = requests.get(self.API_URL, {self.API_PARAM_QUERY: keywords}, timeout=self.timeout) # raises ConnectionError / Timeout exception
        if r.status_code != 200:
            raise SearchEngineResponseException('Expected response code 200, but is {}'.format(r.status_code))
        return self.__get_results(r.text, limit=limit)

    def __get_results(self, html, limit=None):
        '''
        Parses all search results items in the given HTML.
        
        :param html: HTML page
        :return: 
        '''
        results = []
        soup = BeautifulSoup(html, 'lxml')
        for link in soup.findAll(self.CSS_RESULT_ELEMENT, href=self.CSS_RESULT_ELEMENT_HREF):
            results.append(self.__get_result_item(link))
            if len(results) > limit:
                break
        return results
                
    def __get_result_item(self, html_a_element):
        '''
        Parses the HTML a element of a search result
        
        :param html_a_element: HTML a element of the search results
        :return: Array of dictionary {'url': <url>, 'title': <result title>, 'type': <''|'pdf'|...>, 'title_matching': <matching words in result title> }
        '''
        url = html_a_element.get('href')
        if url:
            title = html_a_element.text
            soup = BeautifulSoup(str(html_a_element), 'lxml')
            title_matching = ' '.join([keyword.text.lower() for keyword in soup.find_all(self.CSS_RESULT_ELEMENT_MATCHING_KEYWORDS)])
            #type = soup.find(self.CSS_RESULT_TYPE_ELEMENT, class_=self.CSS_RESULT_TYPE_ELEMENT_CLASS)
            #if type:
            #    type = type.text
            #    title = title.replace(type + ' ', '')
            #    type = type.lower()
        return {'url': url, 'title': title, 'type': self.API_PARAM_FILETYPE_PDF, 'title_matching': title_matching}
