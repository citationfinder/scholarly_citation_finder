import unittest
from .Extractor import Extractor
import config

class ExtractorTest(unittest.TestCase):


    def setUp(self):
        self.extractor = Extractor('test_extractor')


    def test_extract(self):
        first = self.extractor.extract(config.TEST_PATH+'harvester/citeseerx/publication-0.xml')
        self.assertEqual(first, True)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()