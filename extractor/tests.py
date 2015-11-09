from django.test import TestCase

from search_for_citations.models import Citation, Publication
from .citeseer.CitationExtractor import CitationExtractor
# Create your tests here.

        
class CitationExractorTest(TestCase):

    TEST_DIR = 'test/extractor/citeseer/2/'
    TEST_FILE_CITATIONS = TEST_DIR + 'citations.xml'
    TEST_FILE_CITATIONS_COUNT = 5
    
    def setUp(self):
        self.publication = Publication(
            source='http://bonda.cnuce.cnr.it/Documentation/Papers/file-BMCFPS00-DSN2000-76.pdf'
        )
        self.publication.save()
        self.extractor = CitationExtractor(self.publication)
    
    def test_parse_citations(self):
        self.extractor.parse_citations(self.TEST_FILE_CITATIONS)
        citations = Citation.objects.filter(publication=self.publication);
    
        first = len(citations)
        self.assertEqual(first, self.TEST_FILE_CITATIONS_COUNT, 'Shoudl insert %s citations, is %s' % (self.TEST_FILE_CITATIONS_COUNT, first))
