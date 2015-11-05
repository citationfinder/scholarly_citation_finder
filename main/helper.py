import gzip
import os.path
import requests
import shutil

from clint.textui import progress    

def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)

def unzip_file(filename):
    if os.path.isfile(filename):
        print('Unzip %s' % filename)
        inF = gzip.GzipFile(filename, 'rb')
        s = inF.read()
        inF.close()
    else:
        print('No file to unzip!')
        
"""
Downloads a single file. Can handle large files.
"""
def download_file(url, path):
    local_filename = path+url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        print("Downloading %s" % local_filename)
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
        #for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename