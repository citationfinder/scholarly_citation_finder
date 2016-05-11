import requests
import logging
from requests.exceptions import RequestException
from lxml import etree

from scholarly_citation_finder.lib.process import ProcessException
from .CiteseerParser import CiteseerParser

logger = logging.getLogger(__name__)


class CiteseerExtractor:
    '''
    CiteSeerExtractor
    '''

    CITESEER_API_URL = 'http://citeseerextractor.ist.psu.edu:8080/extractor'
    CITESEER_API_FILENAME = 'myfile'
    CITESEER_API_RESPONSE_CITATIONS = 'citations'

    def __init__(self):
        '''
        Create object.
        '''
        self.parser = CiteseerParser('citeseer')

    def extract_file(self, filename):
        '''
        Extract the citations from a provided file.
        
        :param filename: Filename to PDF file
        :raise ProcessException: 
        '''
        logger.info('Extract file: {}'.format(filename))
        try:
            response = self.__call_citeseer_url(self.CITESEER_API_URL, data=open(filename, 'rb').read())
            logger.info(response)
            return self.__extract_references(etree.XML(response))
        except(IOError, ProcessException) as e:
            logger.warn(e, exc_info=True)
            raise ProcessException(e)

    def __extract_references(self, responseAsXml):
        '''
        Extract the references
        
        :param responseAsXml: XML response
        :raise ProcessException:
        '''
        citations_element = responseAsXml.find(self.CITESEER_API_RESPONSE_CITATIONS)
        if citations_element is not None:
            xml = self.__call_citeseer_url(citations_element.text)
            return self.parser.parse(xml)
        else:
            raise ProcessException('Response has no <citations> element')

    def __call_citeseer_url(self, url, data=None):
        '''
        Call a CiteSeer URL

        :param url: URL
        :param data: Data to send 
        :raise ProcessException: 
        '''
        logger.info('Request citeseer url: {}'.format(url))
        try:
            if data:
                resp = requests.post(url, files={self.CITESEER_API_FILENAME: data})
                if resp.status_code != 201:
                    raise ProcessException('Citeseer returned status {} instead of 201\nPossible Error:\n{}'.format(resp.status_code, resp.text))
            else:
                resp = requests.get(url)
                if resp.status_code != 200:
                    raise ProcessException('Citeseer returned status {} instead of 200\nPossible Error:\n{}'.format(resp.status_code, resp.text))
        except(RequestException) as e:
            raise ProcessException('Request to Citeseer server failed: {}'.format(e))
    
        #return resp.text.encode('utf-8')
        return resp.content
