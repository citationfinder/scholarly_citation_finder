#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import logging
import filecmp

from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import download_file, unzip_file, DownloadFailedException, UnzipFailedException

logger = logging.getLogger(__name__)


class DblpDownloader:
    '''
    Helper for downloading the DBLP database.
    '''
    
    DBLP_BASE_URL = 'http://dblp.uni-trier.de/xml/'
    DBLP_FILE_XML_GZ = 'dblp.xml.gz'
    DBLP_FILE_MD5 = 'dblp.xml.gz.md5'
    
    def __init__(self, download_dir):
        '''
        Create object.
        
        :param download_dir: Download directory
        '''
        self.download_dir = download_dir
    
    def download(self):
        '''
        Download database file.
        
        :raise DownloadFailedException: 
        :raise UnzipFailedException:
        :return: File name or false
        '''
        if self.is_new_data_avaible():
            return self.__download_database()
        else:
            return False
     
    def is_new_data_avaible(self):
        '''
        Checks if new data is available:
        Downloads the MD5-file of the XML and compares it with the local stored MD5-file
        
        :return: True, if new data is available  
        '''
        old_md5_file = os.path.join(self.download_dir, self.DBLP_FILE_MD5)
        if os.path.isfile(old_md5_file):
            new_md5_file = download_file(self.DBLP_BASE_URL + self.DBLP_FILE_MD5, config.DOWNLOAD_TMP_DIR)
            if filecmp.cmp(new_md5_file, old_md5_file, shallow=False):
                return False
        return True
    
    def __download_database(self):
        '''
        Downloads the XML- and the DTD-file from DBLP
        
        :return: Filename of the downloaded and unzipped XML database

        :raise DownloadFailedException:
        :raise UnzipFailedException:  
        '''
        logger.info('Download (and unzip) data')
        download_file(self.DBLP_BASE_URL + self.DBLP_FILE_MD5, self.download_dir)
        download_file(self.DBLP_BASE_URL + 'dblp.dtd', self.download_dir)
        
        try:
            xml_database_file = download_file(self.DBLP_BASE_URL + self.DBLP_FILE_XML_GZ, self.download_dir)
            return unzip_file(xml_database_file)
        except(DownloadFailedException, UnzipFailedException) as e:
            raise e
