import unittest
from ..common.Harvester import Harvester,check_author_name

class HarvesterTest(unittest.TestCase):

    def setUp(self):
        self.harvester = Harvester()
        
    def testHarvest(self):
        first = self.harvester.parse_publication(title="Hey", authors=['Na na'])
        self.assertEqual(first, True)
        
class AuthorNameTest(unittest.TestCase):
    
    def test_check_author_name_blacklist(self):
        first = check_author_name('University Oslo')
        self.assertEqual(first, False)
        
    def test_check_author_name_single_word(self):
        first = check_author_name('Jr.')
        self.assertEqual(first, False)  
