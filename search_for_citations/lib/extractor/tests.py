import os.path
from django.test import TestCase

import search_for_citations.config
from .Extractor import Extractor

"""
class ExtractorTest(TestCase):

    SAMPLE_XML = os.path.join(config.TEST_DIR, 'harvester', 'citeseerx', 'publication-0.xml')

    def setUp(self):
        self.extractor = Extractor('test')

    def test_extract(self):
        first = self.extractor.extract_from_xml_file(self.SAMPLE_XML, None)
        self.assertEqual(first, True)
"""
