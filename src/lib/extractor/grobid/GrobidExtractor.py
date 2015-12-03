import requests

from ..common.Extractor import Extractor, get_arguments
from core.process_manager.Process import ProcessError
from .TeiParser import TeiParser

class GrobidExtractor(Extractor):
    
    # URL to Grobid service
    GROBID_API = 'http://localhost:8080'
    
    def __init__(self, **kwargs):
        super(GrobidExtractor, self).__init__('grobid', **kwargs)
        self.teiParser = TeiParser('grobid')

    def extract_from_xml_file(self, filename):
        super(GrobidExtractor, self).extract_from_xml_file(filename, self.extract_from_file)

    #result_file_name = '.cite.teiEx
    def extract_from_file(self, filename):
        self.logger.debug("Extract file: {}".format(filename))
        try:
            self._extract_references(open(filename, 'rb').read())
            return True
        except(IOError, ProcessError) as e:
            self.logger.warn(str(e))
            return False
    
    def _extract_references(self, data, dep_results=None):
        xml = self._call_grobid_method(data, 'processReferences')
        #return ExtractorResult(xml_result=xml)    
        return self.teiParser.parse(xml=xml, callback_biblstruct=self.parse_citation)
    
    def _call_grobid_method(self, data, method):
        self.logger.debug("Call grobid method: {}".format(method))
        url = '{0}/{1}'.format(self.GROBID_API, method)
        files = {'input': data}
        vars = {}
    
        try:
            resp = requests.post(url, files=files, data=vars)
        except requests.exceptions.RequestException as ex:
            raise ProcessError('Request to Grobid server failed')
    
        if resp.status_code != 200:
            raise ProcessError('Grobid returned status {0} instead of 200\nPossible Error:\n{1}'.format(resp.status_code, resp.text))
    
        # remove all namespace info from xml string
        # this is hacky but makes parsing it much much easier down the road
        #remove_xmlns = re.compile(r'\sxmlns[^"]+"[^"]+"')
        #xml_text = remove_xmlns.sub('', resp.content)
        #   
        #xml = safeET.fromstring(xml_text)    
        return resp.content
    
if __name__ == '__main__':
    file_publications, limit = get_arguments()
    
    extractor = GrobidExtractor(limit=limit)
    if file_publications:
        print (file_publications)
        extractor.extract_from_xml_file(file_publications) 