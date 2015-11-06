import gzip
import os.path
import requests
import shutil
import logging
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from requests.exceptions import ConnectionError, InvalidSchema
from clint.textui import progress    

logger = logging.getLogger()


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)

def unzip_file(filename):
    if os.path.isfile(filename):
        logging.debug('Unzip %s' % filename)
        outfilename = filename[:-3]
        inF = gzip.open(filename, 'rb')
        outF = open(outfilename, 'wb')
        outF.write( inF.read() )
        inF.close()
        outF.close()
        return outfilename
    else:
        logging.warn('No file to unzip!')
        return False
        
"""
Downloads a single file. Can handle large files.
"""
def download_file(url, path):
    local_filename = path+url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        logging.debug("Downloading %s" % local_filename)
        #total_length = int(r.headers.get('content-length'))
        #for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

def url_exits(url):
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