from django.test import TestCase

import config
from .Extractor import Extractor

"""
class ExtractorTest(TestCase):

    SAMPLE_XML = config.TEST_PATH+'harvester/citeseerx/publication-0.xml'

    def setUp(self):
        self.extractor = Extractor('test')

    def test_extract(self):
        first = self.extractor.extract_from_xml_file(self.SAMPLE_XML, None)
        self.assertEqual(first, True)
"""