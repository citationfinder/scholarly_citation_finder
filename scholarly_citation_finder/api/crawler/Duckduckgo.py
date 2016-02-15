#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

class Duckduckgo:
    
    API_URL = 'https://duckduckgo.com/html/'
    CSS_RESULT_ELEMENT = 'a'
    CSS_RESULT_ELEMENT_CLASS = 'large'
    CSS_RESULT_TYPE_ELEMENT = 'span'
    CSS_RESULT_TYPE_ELEMENT_CLASS = 'result__type'
    
    def __init__(self):
        pass
    
    
    def query(self, keywords, filetype='pdf'):
        '''
        
        
        :see: https://duck.co/help/results/syntax
        :see: https://duckduckgo.com/params
        :param keywords:
        :param filetype:
        '''
        
        if filetype:
            keywords = 'filetype:{} {}'.format(filetype, keywords)
        
        r = requests.get(self.API_URL, {'q': keywords})
        if r.status_code != 200:
            raise Exception('Expected response code 200, but is {}'.format(r.status_code))
        
        self.__get_links(r.text)
        
    def __get_links(self, html):
        soup = BeautifulSoup(html, 'lxml')
        for link in soup.findAll(self.CSS_RESULT_ELEMENT, class_=self.CSS_RESULT_ELEMENT_CLASS):
            url, title, type = self.__get_link_items(link)
            print('%s: %s "%s"' % (type, url, title))
                
    def __get_link_items(self, html_a_element):
        url = html_a_element.get('href')
        title = html_a_element.text
        if url:
            soup = BeautifulSoup(str(html_a_element), 'lxml')
            type = soup.find(self.CSS_RESULT_TYPE_ELEMENT, class_=self.CSS_RESULT_TYPE_ELEMENT_CLASS)
            if type:
                type = type.text
        return url, title, type
            
if __name__ == '__main__':
    searchengine = Duckduckgo()
    searchengine.query('kernel completion for learning consensus support vector machines in bandwidth limited sensor networks')
