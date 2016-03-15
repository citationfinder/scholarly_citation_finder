import requests
import logging
from requests.exceptions import RequestException, ConnectionError

from scholarly_citation_finder.lib.process import ProcessException
from .TeiParser import TeiParser
from requests.packages.urllib3.connectionpool import HTTPConnectionPool

logger = logging.getLogger(__name__)

class GrobidServceNotAvaibleException(Exception):
    pass


class GrobidExtractor:
    
    GROBID_API_URL = 'http://localhost:8080/grobid/'

    def __init__(self):
        self.parser = TeiParser('grobid')

    def extract_file(self, filename):
        '''
        Extract the citations from a provided file.
        :param filename: Filename to PDF file
        :raise ProcessException:
        :raise GrobidServceNotAvaibleException: 
        '''
        logger.info('Extract file: {}'.format(filename))
        try:
            return self.__extract_references(open(filename, 'rb').read())
        except(GrobidServceNotAvaibleException) as e:
            raise e
        except(IOError, ProcessException) as e:
            raise ProcessException(e)
    
    def __extract_references(self, data):
        '''

        :param data:
        :raise GrobidServceNotAvaibleException:
        :raise ProcessException: 
        '''
        xml = self.__call_grobid_method(data, 'processReferences')
        return self.parser.parse(xml=xml)

    def __call_grobid_method(self, data, method):
        '''
        
        :param data:
        :param method:
        :raise GrobidServceNotAvaibleException:
        :raise ProcessException: 
        '''
        logger.info('Call grobid method: {}'.format(method))
        url = '{0}/{1}'.format(self.GROBID_API_URL, method)
        files = {'input': data}
        vars = {}
    
        try:
            resp = requests.post(url, files=files, data=vars)
        except (HTTPConnectionPool, RequestException, ConnectionError) as e:
            raise GrobidServceNotAvaibleException(e)
    
        if resp.status_code == 200:
            return resp.content
        else:
            raise ProcessException('Grobid returned status {} instead of 200\nPossible Error:\n{}'.format(resp.status_code, resp.text))
