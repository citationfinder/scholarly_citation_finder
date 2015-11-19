from django.test import TestCase

from .parser import parse_publication, check_author_name
from .dblp.DblpHarvester import DblpHarvester
from search_for_citations.models import Publication

# Create your tests here.

class ParserTest(TestCase):
    """
    def test_insert(self):
        first = parse_publication(
            title='Test Title',
            abstract='Hello world',
            source='my.pdf',
            citeseerx_id='-1',
            authors = ['Author 1']
        )
        self.assertNotEqual(first, False, 'Test insert a publication')  
    """
    
    def  test_check_author_name_blacklist(self):
        first = check_author_name('University Oslo')
        self.assertEqual(first, False)
        
    def  test_check_author_name_single_word(self):
        first = check_author_name('Jr.')
        self.assertEqual(first, False)       
        
class DblpHarvesterTest(TestCase):
    
    TEST_DIR = 'test/harvester/dblp/'
    
    def setUp(self):
        self.harvester = DblpHarvester()
    
    def test_harvest(self):
        num_objects_before = Publication.objects.all().count()
        self.harvester.harvest(self.TEST_DIR + 'dblp_tiny.xml')
        first = Publication.objects.all().count() - num_objects_before
        self.assertEqual(first, 4, 'Test insert 4 publications from DBLP XML file')