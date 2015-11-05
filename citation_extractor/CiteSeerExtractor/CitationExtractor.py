import requests
from StringIO import StringIO
from io import BytesIO

from unidecode import unidecode
from lxml import etree
from harvester.parser import parse_publication
from main.helper import download_file, url_exits

class CitationExtractor:
    
    DOWNLOAD_DIR = 'downloads/tmp/'
    CITESEERX_EXTRACTOR_API = 'http://citeseerextractor.ist.psu.edu:8080/extractor'

    def __init__(self, publication):
        self.publication = publication
    
    def download_file(self, url):
        if (url_exits(url)):
            return download_file(url, self.DOWNLOAD_DIR)
        else:
            #raise Exception('Unvalid URL: '+ str(url))   
            self.publication.source = None
            self.publication.save()
    
    def upload_file_to_extractor(self, filename):
        files = {'myfile': open(filename, 'rb')}
        r = requests.post(self.CITESEERX_EXTRACTOR_API, files=files)
        print('a')
        print(r)
        if r.status_code == 201:
            #print(r.text)
            return etree.XML(str(r.text))
        else:
            return False

    def extract(self, url):
        filename = self.download_file(url)
        response = self.upload_file_to_extractor(filename)
        if len(response):
            self.request_citations(response.find('citations').text)            
            #header = response.find('header').text
            #print(header)
            return True
    
    def request_citations(self, url):
        print(url)
        r = requests.get(url)
        if r.status_code == 200:
            self.parse_citations(BytesIO(r.text.encode('utf-8')))
        else:
            raise Exception('Expected server response 200, it is ' + r.status_code)
        
    def parse_citations(self, xml):
        context = etree.iterparse(xml, html=True)
        self.fast_iter(context)
        return True
    
    def get_element(self, element, tag):
        if element.tag == tag and element.text:
            return element.text
        else:
            return None
            
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
    
            title = self.get_element(elem, 'title')
            date = self.get_element(elem, 'date')
            booktitle = self.get_element(elem, 'booktitle')
            journal = self.get_element(elem, 'journal')
            volume = self.get_element(elem, 'volume')
            pages = self.get_element(elem, 'pages')

    
            if elem.tag == 'citation':
                parse_publication(
                    title=title,
                    authors=author_array,
                    date=date,
                    booktitle=booktitle,
                    journal=journal,
                    volume=volume,
                    pages=pages,                  
                )
                    
                del author_array[:]
     
            # Clear element
            elem.clear()
            while elem.getprevious() is not None:
                if elem.getparent() is not None:
                    del elem.getparent()[0]
        del context
        #clear chunks 