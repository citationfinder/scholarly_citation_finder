import requests
import gzip
import shutil
import os.path
from clint.textui import progress
import filecmp

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

def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


class DblpDatabaseDownloader:
    
    DBLP_BASE_URL = 'http://dblp.uni-trier.de/xml/'
    DBLP_DIR = 'downloads/dblp/'
    DBLP_FILE_XML_GZ = 'dblp.xml.gz'
    DBLP_FILE_MD5 = 'dblp.xml.gz.md5'
    
    def __init__(self):
        create_dir(self.DBLP_DIR)
        
        if self.is_new_data_avaible():
            self.download_database()
        else:
            print('No new data is avaiable')
            
    """
    Checks if new data is avaiable:
    Downloads the MD5-file of the XML and compares it with the local stored MD5-file
    """
    def is_new_data_avaible(self):
        old_md5_file = self.DBLP_DIR + self.DBLP_FILE_MD5
        if os.path.isfile(old_md5_file):
            new_md5_file = download_file(self.DBLP_BASE_URL + self.DBLP_FILE_MD5, '')
            if filecmp.cmp(new_md5_file, old_md5_file, shallow=False):
                return False
        return True
    
    """
    Downloads the XML- and the DTD-file from DBLP
    """
    def download_database(self):
        download_file(self.DBLP_BASE_URL + self.DBLP_FILE_MD5, self.DBLP_DIR);
        download_file(self.DBLP_BASE_URL + 'dblp.dtd', self.DBLP_DIR);
        download_file(self.DBLP_BASE_URL + self.DBLP_FILE_XML_GZ, self.DBLP_DIR);
        # Override old md5 file
        #shutil.move(self.DBLP_FILE_MD5, self.DBLP_DIR + self.DBLP_FILE_MD5)