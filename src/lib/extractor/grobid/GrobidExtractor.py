import requests

from ..common.Extractor import Extractor, get_arguments
from core.process_manager.Process import ProcessError
from .TeiParser import TeiParser
#from core.process_manager.utils import external_process

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
        self.logger.debug('Extract file: {}'.format(filename))
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
    
    """
    def _call_grobid_method2(self, input, method):
        '''
        
        :param input: Directory not file!
        :param method:
        '''
        
        GROBID_VERSION = '0.3.9-SNAPSHOT'
        GROBID_DIR = '/home/neo/code/python/search_for_citations/lib/grobid'
        GROBID_HOME = '{}/grobid-home'.format(GROBID_DIR)
        GROBID_OUTPUT = '/home/neo/code/python/search_for_citations/lib/grobid/grobid-home/config'
        
        #command = "java -Xmx1024m -jar grobid-core-{}.one-jar.jar -gH {} -gP {} -dIn {} -dOut /path/to/output/directory -exe {}".format(GROBID_VERSION, GROBID_HOME, GROBID_PROPERTIES, input, method)
        #command = ['java', '-Xmx1024m', '-jar {}/grobid-core-{}.one-jar.jar'.format(GROBID_JAR, GROBID_VERSION), '-gH {}'.format(GROBID_HOME), '-gP {}'.format(GROBID_PROPERTIES), '-dIn {}'.format(input), '-dOut /path/to/output/directory -exe {}'.format(method)]
        #command = ['java', '-Xmx1024m', '-jar', '{}/grobid-core/target/grobid-core-{}.one-jar.jar'.format(GROBID_DIR, GROBID_VERSION), '-gH', GROBID_HOME, '-gP', GROBID_PROPERTIES, '-dIn', input, '-dOut', '{}/tmp'.format(GROBID_DIR), '-exe', method]
        command = ['java', '-Xmx1024m', '-jar', '{}/grobid-core/target/grobid-core-{}.one-jar.jar'.format(GROBID_DIR, GROBID_VERSION), '-gH', GROBID_HOME, '-gP', '{}/config/grobid.properties'.format(GROBID_HOME), '-dIn', input, '-dOut', GROBID_OUTPUT, '-exe', method]
        (exit_status, stdout, stderr) = external_process(command)
        
        print(exit_status)
        print(stdout)
        print(stderr)
    """

    def _call_grobid_method(self, data, method):
        self.logger.debug('Call grobid method: {}'.format(method))
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