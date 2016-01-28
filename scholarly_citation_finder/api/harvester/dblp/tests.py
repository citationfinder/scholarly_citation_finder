import os.path
from django.test import TestCase

from scholarly_citation_finder import config
from .DblpHarvester import DblpHarvester


class DblpHarvesterTest(TestCase):

    TEST_DIR = os.path.join(config.TEST_DIR, 'harvester', 'dblp')
    TEST_XML = os.path.join(TEST_DIR, 'dblp_tiny.xml')

    def setUp(self):
        self.harvester = DblpHarvester()

    def test_harvest_io_error(self):
        self.assertRaises(IOError, self.harvester.harvest, 'non-existing-file.xml')

    def test_harvest_success(self):
        first = self.harvester.harvest(filename=self.TEST_XML)
        self.assertEqual(first, 5, 'Assert 5 publications to be parsed')
