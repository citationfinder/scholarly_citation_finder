#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase

from file import download_file, unzip_file
from process import ProcessException

class FileTest(TestCase):

    def test_download_file_success(self):
        file = 'Conferences.zip'
        first = download_file(path='https://academicgraph.blob.core.windows.net/graph-2015-11-06/',
                              file=file,
                              cwd=None)
        self.assertEqual(first, file)
  
    def test_download_file_wrong_path(self):
        self.assertRaises(ProcessException, download_file, 'https://example.org/', 'non.zip')   
        
"""
class UtilTest(TestCase):
    
    URL_PDF = 'http://www.ronpub.com/publications/OJWT_2014v1i2n02_Kusserow.pdf'
    URL_PDF_2 = 'http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.11.6264&rep=rep1&type=pdf'
    
    EXAMPLE_GZ_FILE = os.path.join(config.TEST_DIR, 'downloads', 'example.pdf.gz')
    
    def test_url_not_well_formed(self):
        first = url_exits('http://example./paper.pdf')
        self.assertEqual(first, False)
    
    #def test_url_does_not_exits(self):
    #    first = url_exits('http://example.org/paper.pdf')
    #    self.assertEqual(first, False)
       
    #def test_pdf_exits(self):
    #    first = url_exits('http://www.informatik.uni-bremen.de/agra/doc/work/evohot04.pdf')
    #    self.assertEqual(first, True)
    
    def test_download_file(self):
        filename = download_file(self.URL_PDF, config.TEST_DIR)
        first = os.path.isfile(filename);
        self.assertEqual(first, True)
        os.remove(filename)
        
    def test_download_file2(self):
        filename = download_file(self.URL_PDF_2, config.TEST_DIR, 'test.pdf')
        first = os.path.isfile(filename);
        self.assertEqual(first, True)
        os.remove(filename)
    

    #def test_unzip_file(self):
    #    filename = unzip_file(self.EXAMPLE_GZ_FILE)
    #    first = os.path.isfile(filename);
    #    if first:
    #        os.remove(filename)
    #    self.assertEqual(first, True)
"""