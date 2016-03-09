import requests
import logging
from requests.exceptions import RequestException

from scholarly_citation_finder.lib.process import ProcessException
from .TeiParser import TeiParser

logger = logging.getLogger(__name__)


class GrobidExtractor:
    
    GROBID_API_URL = 'http://localhost:8080'

    def __init__(self):
        self.parser = TeiParser('grobid')

    def extract_file(self, filename):
        '''
        Extract the citations from a provided file.
        :param filename: Filename to PDF file
        :raise ProcessException: 
        '''
        logger.info('Extract file: {}'.format(filename))
        try:
            return self.__extract_references(open(filename, 'rb').read())
        except(IOError, ProcessException) as e:
            raise ProcessException(e)
    
    def __extract_references(self, data):
        '''
        
        :param data:
        :raise ProcessException: 
        '''
        xml = self.__call_grobid_method(data, 'processReferences')
        return self.parser.parse(xml=xml)

    def __call_grobid_method(self, data, method):
        '''
        
        :param data:
        :param method:
        :raise ProcessException: 
        '''
        logger.info('Call grobid method: {}'.format(method))
        url = '{0}/{1}'.format(self.GROBID_API_URL, method)
        files = {'input': data}
        vars = {}
    
        try:
            resp = requests.post(url, files=files, data=vars)
        except (RequestException) as e:
            raise ProcessException('Request to Grobid server failed: {}'.format(e))
    
        if resp.status_code == 200:
            return resp.content
        else:
            raise ProcessException('Grobid returned status {} instead of 200\nPossible Error:\n{}'.format(resp.status_code, resp.text))
