#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

class WrongResponseException(Exception):
    pass

class Duckduckgo:
    
    API_URL = 'https://duckduckgo.com/html/'
    
    API_PARAM_QUERY = 'q'

    CSS_RESULT_ELEMENT = 'a'
    CSS_RESULT_ELEMENT_CLASS = 'large'
    CSS_RESULT_ELEMENT_MATCHING_KEYWORDS = 'b'
    CSS_RESULT_TYPE_ELEMENT = 'span'
    CSS_RESULT_TYPE_ELEMENT_CLASS = 'result__type'
    
    def __init__(self):
        pass
    
    def __match_title(self, original_title, found_title_matching):
        '''
        
        :param original_title:
        :param found_title_matching:
        '''
        
        num_words_orignal = len(original_title[:58].split(' '))
        num_words_found = len(found_title_matching.split(' '))
        return abs(num_words_orignal-num_words_found) < 2
    
    def query_publication(self, title):
        '''
        Find the PDF for the given publication title.
        
        :param title: Title of the publication
        :return: 
        '''
        try:
            title = title.strip()
            results = self.query(keywords=title, filetype='pdf')
            print(results)
            
            if len(results) >= 1:
                result = results[0]
                if self.__match_title(title, result['title_matching']):
                    return result['url'], result['type']
                    
        except(WrongResponseException):
            pass
        
        return False
    
    def query(self, keywords, filetype=None):
        '''
        Query Duckduckgo
        
        :see: https://duck.co/help/results/syntax
        :see: https://duckduckgo.com/params
        :param keywords: Search keywords
        :param filetype: Optional file type, e.g. 'pdf'
        '''
        if filetype:
            keywords = 'filetype:{} {}'.format(filetype, keywords)
        
        r = requests.get(self.API_URL, {self.API_PARAM_QUERY: keywords})
        if r.status_code != 200:
            raise WrongResponseException('Expected response code 200, but is {}'.format(r.status_code))
        return self.__get_links(r.text)

    def __get_links(self, html):
        '''
        Parses all search result items in the given HTML.
        
        :param html: HTML page
        :return: 
        '''
        
        result = []
        soup = BeautifulSoup(html, 'lxml')
        for link in soup.findAll(self.CSS_RESULT_ELEMENT, class_=self.CSS_RESULT_ELEMENT_CLASS):
            result.append(self.__get_link_items(link))
            if len(result) > 2:
                break
        return result
                
    def __get_link_items(self, html_a_element):
        '''
        Parses the HTML a element of a search result
        
        :param html_a_element: HTML a element of the search results
        :return: Array of dictionary {'url': <url>, 'title': <result title>, 'type': <''|'pdf'|...>, 'title_matching': <matching words in result title> }
        '''
        url = html_a_element.get('href')
        title = html_a_element.text
        if url:
            soup = BeautifulSoup(str(html_a_element), 'lxml')
            title_matching = ' '.join([keyword.text.lower() for keyword in soup.find_all(self.CSS_RESULT_ELEMENT_MATCHING_KEYWORDS)])
            type = soup.find(self.CSS_RESULT_TYPE_ELEMENT, class_=self.CSS_RESULT_TYPE_ELEMENT_CLASS)
            if type:
                type = type.text
                title = title.replace(type + ' ', '')
        return {'url': url, 'title': title, 'type': type.lower(), 'title_matching': title_matching}
            
if __name__ == '__main__':
    searchengine = Duckduckgo()
    r = searchengine.query_publication('kernel completion for learning consensus support vector machines in bandwidth limited sensor networks')
    print(r)
