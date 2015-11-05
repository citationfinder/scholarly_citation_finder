from django.test import TestCase

from .CiteSeerExtractor.CitationExtractor import CitationExtractor
# Create your tests here.

TEST_DIR = 'test/'
        
class CitationExractorTest(TestCase):
    
    TEST_DIR_FILES = TEST_DIR + 'citeseer_extractor_response/'
    
    def setUp(self):
        self.extractor = CitationExtractor(None)
    
    def test_parse_citations(self):
        first = self.extractor.parse_citations(self.TEST_DIR_FILES + 'citations.xml')
        self.assertEqual(first, True)
