import gzip
import os.path
import requests
import shutil
import logging
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from requests.exceptions import ConnectionError, InvalidSchema
from requests.packages.urllib3.connectionpool import HTTPConnectionPool

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
def download_file(url, path=None, name=None):
    if name:
        local_filename = os.path.join(path, name)
    else:
        local_filename = os.path.join(path, url.split('/')[-1])
    try:
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            logging.debug('Downloading %s' % local_filename)
            #total_length = int(r.headers.get('content-length'))
            #for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush() commented by recommendation from J.F.Sebastian
        return local_filename
    except(ConnectionError, InvalidSchema):
        return False

def upload_file(url, filename, status_code = 201):
    logger.debug('Upload {} [{}]'.format(filename, url))
    if not os.path.isfile(filename):
        logger.debug('{} is not a file'.format(filename))
        return False
    
    try:
        files = {'myfile': open(filename, 'rb')}
        r = requests.post(url, files=files)
        if r.status_code == status_code:
            return str(r.text)
        else:
            logger.warn('expected {} as status code, but was {}'.format(status_code, r.status_code))
    except(ConnectionError):
        logger.debug('Connection to {} failed'.format(url))
        return False      
    
    #if os.path.isfile(filename):
    #else:
    #    logger.debug("%s is not a file" % filename)
    #return False

def url_exits(url, check_exists=False):
    #validate = URLValidator(verify_exists=True)
    try:
        validate = URLValidator()
        validate(url)
        if check_exists:
            response = requests.get(url)
            return response.status_code < 400
        else:
            return True
    except(ValidationError):
        return False
    except(ConnectionError, InvalidSchema):
        return False