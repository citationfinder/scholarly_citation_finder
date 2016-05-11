import requests
import logging
from requests.exceptions import RequestException, ConnectionError
from requests.packages.urllib3.connectionpool import HTTPConnectionPool

from scholarly_citation_finder.lib.process import ProcessException
from .TeiParser import TeiParser
from ..Extractor import Extractor, ExtractorNotAvaiableException

logger = logging.getLogger(__name__)


class GrobidExtractor(Extractor):
    '''
    Grobid extractor.
    '''
    
    GROBID_API_URL = 'http://localhost:8080'

    def __init__(self):
        '''
        Create object.
        '''
        self.parser = TeiParser('grobid')

    def extract_file(self, filename, completely=False):
        '''
        Extract the citations from a provided file.
        
        :param filename: Filename to PDF file
        :raise ProcessException: When extractor failed
        :raise ExtractorNotAvaiableException: When extractor is not available
        :raise TeiParserNoReferences: When document has no references
        :raise TeiParserNoDocumentTitle: When document has no title   
        '''
        logger.info('Extract file: {}'.format(filename))
        try:
            file = open(filename, 'rb').read()
            if completely:
                return self.__extract_document(file)
            else:
                return self.__extract_references(file)
        except(IOError, ProcessException) as e:
            raise ProcessException(e)

    def __extract_document(self, data):
        '''
        Call Grobid method to extract the full document.

        :param data:
        :raise ExtractorNotAvaiableException:
        :raise ProcessException: 
        :raise TeiParserNoReferences
        :raise TeiParserNoDocumentTitle
        '''
        xml = self.__call_grobid_method(data, 'processFulltextDocument')
        return self.parser.parse_document(xml=xml)

    def __extract_references(self, data):
        '''
        Call Grobid method to extract the references of the document.
        
        :param data:
        :raise ExtractorNotAvaiableException:
        :raise ProcessException: 
        '''
        xml = self.__call_grobid_method(data, 'processReferences')
        return self.parser.parse_references(xml=xml)

    def __call_grobid_method(self, data, method):
        '''
        Call a Grobid method.
        
        :param data: Data to send to grobid
        :param method: Grobid method
        :raise ExtractorNotAvaiableException:
        :raise ProcessException: 
        '''
        logger.info('Call grobid method: {}'.format(method))
        url = '{0}/{1}'.format(self.GROBID_API_URL, method)
        files = {'input': data}
        vars = {}
    
        try:
            resp = requests.post(url, files=files, data=vars)
        except (HTTPConnectionPool, RequestException, ConnectionError) as e:
            raise ExtractorNotAvaiableException(e)
    
        if resp.status_code == 200:
            return resp.content
        else:
            raise ProcessException('Grobid returned status {} instead of 200\nPossible Error:\n{}'.format(resp.status_code, resp.text))
