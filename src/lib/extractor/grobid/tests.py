#!/usr/bin/python
# -*- coding: utf-8 -*
import os.path
from django.test import TestCase

import config
from .GrobidExtractor import GrobidExtractor

"""
class GrobidExtractorTest(TestCase):

    TEST_PDF = os.path.join(config.TEST_DIR, 'paper', 'OJWT_2014v1i2n02_Kusserow.pdf')

    def setUp(self):
        self.extractor = GrobidExtractor()

    def test_extract_from_file(self):
        first = self.extractor.extract_from_file(self.TEST_PDF)
        self.assertEqual(first, True)
"""