from io import BytesIO
from lxml import etree
from lxml.etree import XMLSyntaxError
import requests

from lib.utils import upload_file
from ..common.Extractor import Extractor

class CiteseerExtractor(Extractor):
    
    #CITESEER_EXTRACTOR_API = 'http://citeseerextractor.ist.psu.edu:8080/extractor'
    CITESEER_EXTRACTOR_API = 'http://localhost:8081/extractor'

    def __init__(self, **kwargs):
        super(CiteseerExtractor, self).__init__('citeseer', **kwargs)

    def extract_from_xml_file(self, filename):
        super(CiteseerExtractor, self).extract_from_xml_file(filename, self.extract_from_file)
    
    def extract_from_file(self, filename):
        self.logger.debug("Extract %s" % filename)
        response = upload_file(self.CITESEER_EXTRACTOR_API, filename)
        if response:
            responseAsXml = etree.XML(response)
            return self.request_citations(responseAsXml.find('citations').text)            
        else:
            return False
        
    def request_citations(self, url):
        self.logger.debug("Request %s" % url)
        r = requests.get(url)
        if r.status_code == 200:
            return self.parse_citations(BytesIO(r.text.encode('utf-8')))
        else:
            self.logger.debug('request_citations Expected server response 200, it is {}'.format(r.status_code))
            return False
        
    def parse_citations(self, xml):
        self.logger.debug("Parse citations")
        try:
            context = etree.iterparse(xml, html=False)
            self.fast_iter(context)
            return True
        except XMLSyntaxError as e:
            self.logger.debug(str(e))
            return False
    
    def get_element(self, element, tag, variable):
        if element.tag == tag and element.text:
            return self._escape_text(element.text)
        return variable
    
    def _escape_text(self, text):
        # TODO: .replace('&', '&amp;') destroys other symbols like "&lt;", which are already escaped
        return text.replace('<', '&lt;').replace('>', '&gt;')
            
    def fast_iter(self, context, *args, **kwargs):
        
        title = ''
        date = ''
        booktitle = ''
        journal = ''
        volume = ''
        #number
        pages = ''
        #publisher
        #abstract = ''
        author_array = []
        
        citation_context = ''
    
        #read chunk line by line
        #we focus author and title
        for _, elem in context:
            if elem.tag == 'author' and elem.text:
                author_array.append(self._escape_text(elem.text))
    
            title = self.get_element(elem, 'title', title)
            date = self.get_element(elem, 'date', date)
            booktitle = self.get_element(elem, 'booktitle', booktitle)
            journal = self.get_element(elem, 'journal', journal)
            volume = self.get_element(elem, 'volume', volume)
            pages = self.get_element(elem, 'pages', pages)
            citation_context = self.get_element(elem, 'context', citation_context)

            #if elem.tag == 'context':
            #    context = elem.text
    
            if elem.tag == 'citation':
                self.parse_citation(
                    context = citation_context,
                    title=title,
                    authors=author_array,
                    date=date,
                    booktitle=booktitle,
                    journal=journal,
                    volume=volume,
                    pages=pages,
                    extractor=self.name             
                )
                    
                del author_array[:]
     
            # Clear element
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context
        #clear chunks