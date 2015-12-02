from django.test import TestCase
from lib.extractor.citeseer.CiteseerExtractor import CiteseerExtractor
import config
import os.path

class CiteseerExtractorTest(TestCase):

    TEST_DIR = os.path.join(config.TEST_DIR, 'extractor', 'citeseer', '2')
    TEST_FILE_CITATIONS = os.path.join(TEST_DIR, 'citations.xml')
    TEST_FILE_CITATIONS_COUNT = 5
    
    TEST_PDF = os.path.join(config.TEST_DIR, 'paper', 'OJWT_2014v1i2n02_Kusserow.pdf')
    TEST_FILELIST = os.path.join(config.TEST_DIR, 'harvester', 'citeseerx', 'publication-0.xml')
    
    def setUp(self):
        self.extractor = CiteseerExtractor()

    #def test_extract_from_file(self):
    #    self.extractor.output.open('{}.tmp.xml'.format(self.TEST_FILELIST[:-4])) # TODO: not really good
    #    first = self.extractor.extract_from_file(self.TEST_PDF)
    #    self.assertEquals(first, True)
    
    def test_extract_from_xml_file(self):
        self.extractor.extract_from_xml_file(self.TEST_FILELIST)
        first = os.path.isfile('{}.tmp.xml'.format(self.TEST_FILELIST[:-4]))
        self.assertEqual(first, True)
    
    #def test_parse_citations(self):
    #    self.extractor.parse_citations(self.TEST_FILE_CITATIONS)
    #    #self.assertEqual(first, self.TEST_FILE_CITATIONS_COUNT, 'Shoudl insert %s citations, is %s' % (self.TEST_FILE_CITATIONS_COUNT, first))
