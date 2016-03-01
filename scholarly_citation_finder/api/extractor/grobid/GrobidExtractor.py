import requests
import logging

from scholarly_citation_finder.lib.process import ProcessException
from TeiParser import TeiParser
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


class GrobidExtractor:
    
    # URL to Grobid service
    GROBID_API = 'http://localhost:8080'

    def __init__(self, **kwargs):
        self.teiParser = TeiParser('grobid')

    def extract_file(self, filename):
        '''
        Extract the citations from a provied file.
        
        :param filename: Path to PDF file
        '''
        logger.debug('Extract file: {}'.format(filename))
        try:
            return self.__extract_references(open(filename, 'rb').read())
        except(IOError, ProcessException) as e:
            logger.warn(e, exc_info=True)
            return False
    
    def __extract_references(self, data):
        xml = self.__call_grobid_method(data, 'processReferences')
        return self.teiParser.parse(xml=xml,
                                    callback_biblstruct=None)

    def __call_grobid_method(self, data, method):
        logger.debug('Call grobid method: {}'.format(method))
        url = '{0}/{1}'.format(self.GROBID_API, method)
        files = {'input': data}
        vars = {}
    
        try:
            resp = requests.post(url, files=files, data=vars)
        except (RequestException) as e:
            raise ProcessException('Request to Grobid server failed: {}'.format(e))
    
        if resp.status_code != 200:
            raise ProcessException('Grobid returned status {0} instead of 200\nPossible Error:\n{1}'.format(resp.status_code, resp.text))
    
        # remove all namespace info from xml string
        # this is hacky but makes parsing it much much easier down the road
        #remove_xmlns = re.compile(r'\sxmlns[^"]+"[^"]+"')
        #xml_text = remove_xmlns.sub('', resp.content)
        #
        #xml = safeET.fromstring(xml_text)
        return resp.content
