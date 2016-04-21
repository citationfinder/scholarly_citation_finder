#!/usr/bin/python
# -*- coding: utf-8 -*-
from scholarly_citation_finder.tools.nameparser.StringMatching import nearly_match


class SearchEngineResponseException(Exception):
    pass


class SearchEngine(object):
    
    def __init__(self, timeout=1.5):
        '''
        
        :param timeout: Request timeout in seconds
        '''
        self.timeout = timeout
        
    def query(self, keywords, filetype=None, limit=None):
        '''
        Query search engine
        
        :see: https://duck.co/help/results/syntax
        :see: https://duckduckgo.com/params
        :param keywords: Search keywords
        :param filetype: Optional file type, e.g. 'pdf'
        :raise SearchEngineResponseException: 
        :raise ConnectionError:
        :raise Timeout: When engine does not responds. A reason can be that the server stops responding after too many requests.
        '''
        raise Exception('Implement this method')

    def nearly_match_titles(self, original, found):
        if found.endswith(self.TRUNCATE_STRING):
            found = found.rstrip(self.TRUNCATE_STRING).rstrip()
            original = original[:len(found)]
        return nearly_match(original.lower(), found.lower(), minimum_ratio=0.75)
