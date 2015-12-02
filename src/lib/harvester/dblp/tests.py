import unittest
from .DblpHarvester import DblpHarvester
import os.path
import config

class DblpHarvesterTest(unittest.TestCase):

    DOWNLOAD_DIR = '../downloads/'
    TEST_DIR = os.path.join(config.TEST_DIR, 'harvester', 'dblp/')

    def setUp(self):
        self.harvester = DblpHarvester()
        
    def test_harvest_io_error(self):
        self.assertRaises(IOError, self.harvester.harvest, 'non-existing-file.xml')

    def test_harvest_file_creation(self):
        self.harvester.harvest(self.TEST_DIR + 'dblp_tiny.xml')
        first = os.path.isfile(os.path.join(config.DOWNLOAD_DIR, 'harvester', 'dblp', 'publication-0.xml'))
        self.assertEqual(first, True)
        
    """
    def test_harvest(self):
        self.harvester.harvest(self.TEST_DIR + 'dblp_tiny.xml')
        #self.assertEqual(first, 4, 'Test insert 4 publications from DBLP XML file')
    """