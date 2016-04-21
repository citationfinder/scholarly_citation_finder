
class SearchEngineResponseException(Exception):
    pass


class SearchEngine():
    
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
        :raise Timeout: 
        '''
        raise Exception('Not implemented')
