from django.test import TestCase
import os.path
from .helper import url_exits, download_file, unzip_file
# Create your tests here.

class HelperTest(TestCase):
    
    EXAMPLE_GZ_FILE = 'test/downloads/example.pdf.gz'
    
    def test_url_not_well_formed(self):
        first = url_exits('http://example./paper.pdf')
        self.assertEqual(first, False)    
    
    def test_url_does_not_exits(self):
        first = url_exits('http://example.org/paper.pdf')
        self.assertEqual(first, False)
        
    #def test_pdf_exits(self):
    #    first = url_exits('http://www.informatik.uni-bremen.de/agra/doc/work/evohot04.pdf')
    #    self.assertEqual(first, True)    
    
    #def test_download_file(self):
    #    filename = download_file('http://www.ronpub.com/publications/OJWT_2014v1i2n02_Kusserow.pdf', 'test/')
    #    first = os.path.isfile(filename);
    #    self.assertEqual(first, True)
    
    def test_unzip_file(self):
        filename = unzip_file(self.EXAMPLE_GZ_FILE)
        first = os.path.isfile(filename);
        if first:
            os.remove(filename)
        self.assertEqual(first, True)