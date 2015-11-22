import requests
from io import BytesIO

from lxml import etree
from ...utils import upload_file

from ..common.Extractor import Extractor

import logging
from lxml.etree import XMLSyntaxError

class CiteseerExtractor(Extractor):
    
    #CITESEERX_EXTRACTOR_API = 'http://citeseerextractor.ist.psu.edu:8080/extractor'
    CITESEERX_EXTRACTOR_API = 'http://localhost:8080/extractor'

    def __init__(self):
        super(CiteseerExtractor, self).__init__('citeseer')

    def extract_from_xml_file(self, filename):
        super(CiteseerExtractor, self).extract_from_xml_file(filename, self.extract_from_file)
    
    def extract_from_file(self, filename):
        self.logger.debug("Extract %s" % filename)
        self.open_output_file('{}.xml'.format(filename))
        response = upload_file(self.CITESEERX_EXTRACTOR_API, filename)
        if response:
            responseAsXml = etree.XML(response)
            self.request_citations(responseAsXml.find('citations').text)            
            return True
        else:
            return False
        
    def request_citations(self, url):
        self.logger.debug("Request %s" % url)
        r = requests.get(url)
        if r.status_code == 200:
            self.parse_citations(BytesIO(r.text.encode('utf-8')))
        else:
            raise Exception('request_citations Expected server response 200, it is ' + r.status_code)
        
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
            return element.text
        return variable
            
    def fast_iter(self, context, *args, **kwargs):
        #xml categories
        title = ''
        author_array = []
        date = ''
        booktitle = ''
        journal = ''
        volume = ''
        pages = ''
        #date = ''
        #journal
        #volume
        #abstract = ''
        citation_context = ''
    
        #read chunk line by line
        #we focus author and title
        for event, elem in context:
            if elem.tag == 'author':
                author_array.append(elem.text)
    
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
                    extractor='citeseer'                  
                )
                    
                del author_array[:]
     
            # Clear element
            elem.clear()
            while elem.getprevious() is not None:
                #if elem.getparent() is not None:
                del elem.getparent()[0]
        del context
        #clear chunks 