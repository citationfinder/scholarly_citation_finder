import os.path
import filecmp

from ....lib.file import download_file, unzip_file
from ..Harvester import Harvester


class DblpDownloader(Harvester):
    
    DBLP_BASE_URL = 'http://dblp.uni-trier.de/xml/'
    DBLP_FILE_XML_GZ = 'dblp.xml.gz'
    DBLP_FILE_MD5 = 'dblp.xml.gz.md5'
    
    def __init__(self):
        super(DblpDownloader, self).__init__('dblp')
    
    def download(self):
        if self.is_new_data_avaible():
            return self._download_database()
        else:
            self.logger.info('No new data is avaiable')
            return False
     
    def is_new_data_avaible(self):
        '''
        Checks if new data is avaiable:
        Downloads the MD5-file of the XML and compares it with the local stored MD5-file        
        '''
        self.logger.debug('Check is new data avaiable')
        old_md5_file = os.path.join(self.download_dir, self.DBLP_FILE_MD5)
        if os.path.isfile(old_md5_file):
            new_md5_file = download_file(self.DBLP_BASE_URL + self.DBLP_FILE_MD5, '')
            if filecmp.cmp(new_md5_file, old_md5_file, shallow=False):
                return False
        return True
    
    def _download_database(self):
        '''
        Downloads the XML- and the DTD-file from DBLP        
        '''
        self.logger.info('Download (and unzip) data')
        download_file(self.DBLP_BASE_URL + self.DBLP_FILE_MD5, self.download_dir)
        download_file(self.DBLP_BASE_URL + 'dblp.dtd', self.download_dir)
        xml_database_file = download_file(self.DBLP_BASE_URL + self.DBLP_FILE_XML_GZ, self.download_dir)
        
        if xml_database_file:
            return unzip_file(xml_database_file)
        else:
            return False
