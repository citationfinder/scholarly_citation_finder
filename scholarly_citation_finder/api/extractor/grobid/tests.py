#!/usr/bin/python
# -*- coding: utf-8 -*
import os.path
from django.test import TestCase

from scholarly_citation_finder import config
from .GrobidExtractor import GrobidExtractor
from .TeiParser import TeiParser


class GrobidExtractorTest(TestCase):

    TEST_PDF = os.path.join(config.TEST_DIR, 'paper', 'OJWT_2014v1i2n02_Kusserow.pdf')

    def setUp(self):
        self.extractor = GrobidExtractor()

    def test_extract_from_file(self):
        first = self.extractor.extract_file(self.TEST_PDF)
        self.assertEqual(first, True)

class TeiParserTest(TestCase):
    
    TMP_OUTPUT_FILE = os.path.join(config.TEST_DIR, 'tmp.xml')
    SAMPLE_TEI_CITATION_FILE = os.path.join(config.TEST_DIR, 'extractor', 'grobit', 'references.xml')
    
    def setUp(self):
        self.parser = TeiParser()
        
    def test_parse(self):
        result = self.parser.parse(open(self.SAMPLE_TEI_CITATION_FILE).read())
        
        self.assertEqual(len(result), 2)
        
        # check title
        self.assertEqual(result[0]['publication']['title'], 'Example title')
        self.assertEqual(result[1]['publication']['title'], 'Another pub')
        # check author
        self.assertEqual(result[0]['authors'][0], 'Cluster,A B')
        self.assertEqual(result[0]['authors'][1], 'Cabrerizo,F')
        # check publication infos
        self.assertEqual(result[0]['publication']['volume'], '3')
        self.assertEqual(result[0]['publication']['pages_from'], '161')
        self.assertEqual(result[0]['publication']['pages_to'], '168')
        self.assertEqual(result[0]['publication']['year'], '2009')
        
        # confernce and journal name        
        self.assertEqual(result[0]['conference_instance_name'], 'Example conference')
        self.assertEqual(result[1]['journal_name'], 'Example journal')
