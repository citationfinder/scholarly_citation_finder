from django.test import TestCase
from lib.extractor.citeseer.CiteseerExtractor import CiteseerExtractor
import config
import os.path

class CiteseerExtractorTest(TestCase):

    TEST_DIR = config.TEST_PATH+'extractor/citeseer/2/'
    TEST_FILE_CITATIONS = TEST_DIR + 'citations.xml'
    TEST_FILE_CITATIONS_COUNT = 5
    
    TEST_PDF = config.TEST_PATH+'paper/OJWT_2014v1i2n02_Kusserow.pdf';
    TEST_FILELIST = config.TEST_PATH+'harvester/citeseerx/publication-0.xml'
    
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
