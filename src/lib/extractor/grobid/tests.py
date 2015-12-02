#!/usr/bin/python
# -*- coding: utf-8 -*
import os.path
from io import BytesIO
from django.test import TestCase

import config
from .GrobidExtractor import GrobidExtractor
from .TeiParser import TeiParser

"""
class GrobidExtractorTest(TestCase):

    TEST_PDF = os.path.join(config.TEST_DIR, 'paper', 'OJWT_2014v1i2n02_Kusserow.pdf')

    def setUp(self):
        self.extractor = GrobidExtractor()

    def test_extract_from_file(self):
        first = self.extractor.extract_from_file(self.TEST_PDF)
        self.assertEqual(first, True)
"""

class TeiParserTest(TestCase):
    
    TMP_OUTPUT_FILE = os.path.join(config.TEST_DIR, 'tmp.xml')
    SAMPLE_TEI_CITATION_FILE = os.path.join(config.TEST_DIR, 'extractor', 'gropit', 'references.xml')
    
    def setUp(self):
        self.parser = TeiParser()
        
    def test_parse(self):
        self.parser.output.open(self.TMP_OUTPUT_FILE)
        self.parser.parse(self.SAMPLE_TEI_CITATION_FILE)
        self.parser.output.close()