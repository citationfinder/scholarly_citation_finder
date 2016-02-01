import requests

from scholarly_citation_finder.lib.process import ProcessException
from scholarly_citation_finder.api.Parser import Parser
from TeiParser import TeiParser


class GrobidExtractor(Parser):
    
    # URL to Grobid service
    GROBID_API = 'http://localhost:8080'
    

    def __init__(self, **kwargs):
        super(GrobidExtractor, self).__init__('grobid', **kwargs)
        self.teiParser = TeiParser('grobid')


    def extract_file(self, filename):
        '''
        Extract the citations from a provied file.
        
        :param filename: Path to PDF file
        '''
        self.logger.debug('Extract file: {}'.format(filename))
        try:
            self._extract_references(open(filename, 'rb').read())
            return True
        except(IOError, ProcessException) as e:
            self.logger.warn(e, exc_info=True)
            return False
    
    def _extract_references(self, data, dep_results=None):
        xml = self._call_grobid_method(data, 'processReferences')
        return self.teiParser.parse(xml=xml,
                                    callback_biblstruct=self.parse_publication_reference)

    def _call_grobid_method(self, data, method):
        self.logger.debug('Call grobid method: {}'.format(method))
        url = '{0}/{1}'.format(self.GROBID_API, method)
        files = {'input': data}
        vars = {}
    
        try:
            resp = requests.post(url, files=files, data=vars)
        except (requests.exceptions.RequestException) as ex:
            raise ProcessException('Request to Grobid server failed')
    
        if resp.status_code != 200:
            raise ProcessException('Grobid returned status {0} instead of 200\nPossible Error:\n{1}'.format(resp.status_code, resp.text))
    
        # remove all namespace info from xml string
        # this is hacky but makes parsing it much much easier down the road
        #remove_xmlns = re.compile(r'\sxmlns[^"]+"[^"]+"')
        #xml_text = remove_xmlns.sub('', resp.content)
        #
        #xml = safeET.fromstring(xml_text)
        return resp.content