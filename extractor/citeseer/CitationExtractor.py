import requests
from StringIO import StringIO
from io import BytesIO

from unidecode import unidecode
from lxml import etree
from harvester.parser import parse_publication
from main.helper import download_file, url_exits, upload_file
from django.core.exceptions import ValidationError

import logging
logger = logging.getLogger()

class CitationExtractor:
    
    DOWNLOAD_DIR = 'downloads/tmp/'
    CITESEERX_EXTRACTOR_API = 'http://citeseerextractor.ist.psu.edu:8080/extractor'

    def __init__(self, publication):
        self.publication = publication
        if (url_exits(publication.source)):
            self.url = publication.source # src()
        else:
            logger.warn('Unvalid URL: ' + publication.source)
            raise ValidationError('Unvalid URL')

    def extract(self):
        logger.debug("Extract %s" % self.url)
        # Download file tempoary and upload this file to the extrator
        filename = download_file(self.url, self.DOWNLOAD_DIR)
        response = upload_file(self.CITESEERX_EXTRACTOR_API, filename)
        if response:
            responseAsXml = etree.XML(response)
            self.request_citations(responseAsXml.find('citations').text)            
            #header = response.find('header').text
            #print(header)
            return True
        else:
            return False
    
    def request_citations(self, url):
        logger.debug("Request %s" % url)
        r = requests.get(url)
        if r.status_code == 200:
            self.parse_citations(BytesIO(r.text.encode('utf-8')))
        else:
            raise Exception('Expected server response 200, it is ' + r.status_code)
        
    def parse_citations(self, xml):
        logger.debug("Parse citations")
        context = etree.iterparse(xml, html=False)
        self.fast_iter(context)
        return True
    
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

    
            if elem.tag == 'citation':
                parse_publication(
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