import os.path
import filecmp
import logging

from ...utils import create_dir, download_file, unzip_file

logger = logging.getLogger()

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
            logger.debug('No new data is avaiable')
            
    """
    Checks if new data is avaiable:
    Downloads the MD5-file of the XML and compares it with the local stored MD5-file
    """
    def is_new_data_avaible(self):
        logger.debug('Check is new data avaiable')
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
        logger.debug('Download (and unzip) data')
        download_file(self.DBLP_BASE_URL + self.DBLP_FILE_MD5, self.DBLP_DIR);
        download_file(self.DBLP_BASE_URL + 'dblp.dtd', self.DBLP_DIR);
        download_file(self.DBLP_BASE_URL + self.DBLP_FILE_XML_GZ, self.DBLP_DIR);
        # Override old md5 file
        #shutil.move(self.DBLP_FILE_MD5, self.DBLP_DIR + self.DBLP_FILE_MD5)