import unittest
from .DblpHarvester import DblpHarvester

class DblpHarvesterTest(unittest.TestCase):

    TEST_DIR = '../test/harvester/dblp/'

    def setUp(self):
        self.harvester = DblpHarvester()
        
    def test_harvest_io_error(self):
        self.assertRaises(IOError, self.harvester.harvest, 'wrong-file.xml')

    """
    def test_harvest(self):
        self.harvester.harvest(self.TEST_DIR + 'dblp_tiny.xml')
        #self.assertEqual(first, 4, 'Test insert 4 publications from DBLP XML file')
    """