#!/usr/bin/python
# -*- coding: utf-8 -*
import unittest
from .GrobidExtractor import GrobidExtractor
import config

class GrobidExtractorTest(unittest.TestCase):

    TEST_PDF = config.TEST_PATH+'paper/OJWT_2014v1i2n02_Kusserow.pdf'

    def setUp(self):
        self.extractor = GrobidExtractor()

    """
    def test_extract_from_file(self):
        first = self.extractor.extract_from_file(self.TEST_PDF)
        self.assertEqual(first, True)
    """