import requests
import logging
from requests.exceptions import RequestException
from lxml import etree

from scholarly_citation_finder.lib.process import ProcessException
from .CiteseerParser import CiteseerParser

logger = logging.getLogger(__name__)


class CiteseerExtractor:

    CITESEER_API_URL = 'http://citeseerextractor.ist.psu.edu:8080/extractor'
    CITESEER_API_FILENAME = 'myfile'

    def __init__(self):
        self.parser = CiteseerParser('citeseer')

    def extract_file(self, filename):
        logger.debug('Extract file: {}'.format(filename))
        try:
            response = self.__call_citeseer_url(self.CITESEER_API_URL, data=open(filename, 'rb').read())
            return self.__extract_references(etree.XML(response))
        except(IOError, ProcessException) as e:
            logger.warn(e, exc_info=True)
            return False

    def __extract_references(self, responseAsXml):
        '''
        
        :param responseAsXml:
        :raise: RequestException:
        '''
        xml = self.__call_citeseer_url(responseAsXml.find('citations').text)
        return self.parser.parse(xml)

    def __call_citeseer_url(self, url, data=None):
        '''
        
        :param url:
        :raise RequestException: 
        '''
        logger.debug('Request citeseer url: {}'.format(url))
        try:
            if data:
                files = {self.CITESEER_API_FILENAME: data}
            resp = requests.get(url, files=files)
        except (RequestException) as e:
            raise ProcessException('Request to Citeseer server failed: {}'.format(e))
    
        if resp.status_code not in (200, 201):
            raise ProcessException('Citeseer returned status {} instead of 200/201\nPossible Error:\n{}'.format(resp.status_code, resp.text))
        #return resp.text.encode('utf-8')
        return resp.content