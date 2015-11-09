from django.test import TestCase

from .parser import parse_publication
from .dblp.DblpHarvester import DblpHarvester
from search_for_citations.models import Publication

# Create your tests here.

class ParserTest(TestCase):
    
    def test_insert(self):
        first = parse_publication(
            title='Test Title',
            abstract='Hello world',
            source='my.pdf',
            citeseerx_id='-1',
            authors = ['Author 1']
        )
        self.assertNotEqual(first, False, 'Test insert a publication')    
        
class DblpHarvesterTest(TestCase):
    
    TEST_DIR = 'test/harvester/dblp/'
    
    def setUp(self):
        self.harvester = DblpHarvester()
    
    def test_harvest(self):
        num_objects_before = Publication.objects.all().count()
        self.harvester.harvest(self.TEST_DIR + 'dblp_tiny.xml')
        first = Publication.objects.all().count() - num_objects_before
        self.assertEqual(first, 4, 'Test insert 4 publications from DBLP XML file')