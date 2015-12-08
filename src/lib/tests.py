#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
import os.path
import config
from .utils import url_exits, download_file, unzip_file
# Create your tests here.
from .Parser import Parser

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


class ParserTest(TestCase):

    SAMPLE_XML = os.path.join(config.TEST_DIR, 'harvester', 'test_parser.xml')

    def setUp(self):
        self.parser = Parser('test_parser')
        
    def test_parse_publication(self):
        self.parser.open_output_file(self.SAMPLE_XML)
        first = self.parser.parse_publication(title=u'Hey $äüöé', authors=[u'Na éäüö'])
        self.parser.close_output_file()
        self.assertEqual(first, True)
        os.remove(self.SAMPLE_XML)
    
    def test_check_author_name_blacklist(self):
        first = self.parser.check_author_name('University Oslo')
        self.assertEqual(first, False)
        
    def test_check_author_name_single_word(self):
        first = self.parser.check_author_name('Jr.')
        self.assertEqual(first, False)
