import os.path
from django.test import TestCase

from scholarly_citation_finder import config
from .DblpHarvester import DblpHarvester


class DblpHarvesterTest(TestCase):

    TEST_DIR = os.path.join(config.TEST_DIR, 'harvester', 'dblp')
    TEST_XML = os.path.join(TEST_DIR, 'dblp_tiny.xml')

    def setUp(self):
        self.harvester = DblpHarvester()

    def tearDown(self):
        self.harvester.conn.close()

    def test_harvest_io_error(self):
        self.assertRaises(IOError, self.harvester.harvest, 'non-existing-file.xml')

    def test_harvest_success(self):
        first = self.harvester.harvest(filename=self.TEST_XML)
        self.assertEqual(first, 6, 'Assert 6 publications to be parsed, but is {}'.format(first))

    def test_harvest_success_limit(self):
        first = self.harvester.harvest(filename=self.TEST_XML, limit=2)
        self.assertEqual(first, 2, 'Assert 2 publications to be parsed, but is {}'.format(first))

    def test_harvest_success_from(self):
        first = self.harvester.harvest(filename=self.TEST_XML, _from='journals/puc/ZhouGPRYS11')
        self.assertEqual(first, 3, 'Assert 3 publications to be parsed, but is {}'.format(first))
        