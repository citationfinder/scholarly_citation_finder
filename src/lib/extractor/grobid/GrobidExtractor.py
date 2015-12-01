from ..common.Extractor import Extractor
from core.process_manager.Process import ProcessError
import requests
import re

class GrobidExtractor(Extractor):
    
    # URL to Grobid service
    GROBID_HOST = 'http://localhost:8080'
    
    def __init__(self):
        super(GrobidExtractor, self).__init__('grobid')

    #result_file_name = '.cite.tei'
    def extract_from_file(self, filename):
        self.extract(open(filename, 'rb').read())
    
    def extract(self, data, dep_results=None):
        xml = self._call_grobid_method(data, 'processReferences')
        #return ExtractorResult(xml_result=xml)    
        return xml
    
    def _call_grobid_method(self, data, method):
        url = '{0}/{1}'.format(self.GROBID_HOST, method)
        files = {'input': data}
        vars = {}
    
        try:
            resp = requests.post(url, files=files, data=vars)
        except requests.exceptions.RequestException as ex:
            raise ProcessError('Request to Grobid server failed')
    
        if resp.status_code != 200:
            raise ProcessError('Grobid returned status {0} instead of 200\nPossible Error:\n{1}'.format(resp.status_code, resp.text))
    
        print(resp.content)
        # remove all namespace info from xml string
        # this is hacky but makes parsing it much much easier down the road
        #remove_xmlns = re.compile(r'\sxmlns[^"]+"[^"]+"')
        #xml_text = remove_xmlns.sub('', resp.content)
        #   
        #xml = safeET.fromstring(xml_text)
    
        return resp    