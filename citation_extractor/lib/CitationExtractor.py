from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from requests.exceptions import ConnectionError, InvalidSchema
import requests
from lxml import etree

class CitationExtractor:
    
    DOWNLOAD_DIR = 'downloads/tmp/'
    CITESEERX_EXTRACTOR_API = 'http://citeseerextractor.ist.psu.edu:8080/extractor'
    
    def __init__(self, url):
        if (self.url_exits(url)):
            filename = self.download_file(url)
            self.extract(filename)
        else:
            raise Exception('Unvalid URL: '+ str(url))
            
                
    def url_exits(self, url):
        #validate = URLValidator(verify_exists=True)
        try:
            validate = URLValidator()
            validate(url)
            response = requests.get(url)
            return response.status_code < 400
        except(ValidationError):
            return False
        except(ConnectionError, InvalidSchema):
            return False
        
    def download_file(self, url):
        print('download ' + str(url))
        local_filename = self.DOWNLOAD_DIR+url.split('/')[-1]
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush() commented by recommendation from J.F.Sebastian
        return local_filename
    
    def upload_file_to_extractor(self, filename):
        files = {'myfile': open(filename, 'rb')}
        r = requests.post(self.CITESEERX_EXTRACTOR_API, files=files)
        if r.status_code == 201:
            print(r.text)
            return etree.XML(str(r.text))
        else:
            return False

    def extract(self, filename):
        response = self.upload_file_to_extractor(filename)
        if len(response):
            #token = root.find('token').text
            citations = response.find('citations').text
            print(citations)
            header = response.find('header').text
            print(header)
            return True