#!/usr/bin/python
# -*- coding: utf-8 -*
import unittest
from ..common.Harvester import Harvester,check_author_name

class HarvesterTest(unittest.TestCase):

    def setUp(self):
        self.harvester = Harvester()
        
    def test_harvest(self):
        first = self.harvester.parse_publication(title=u'Hey $äüöé', authors=[u'Na éäüö'])
        self.assertEqual(first, True)

    def test_get_arguments_short_forms(self):
        first = self.harvester.get_arguments(['-l', '20'])
        self.assertEqual(first, 20)
        
    def test_get_arguments_long_forms(self):
        first = self.harvester.get_arguments(['--limit', '20'])
        self.assertEqual(first, 20)

        
class AuthorNameTest(unittest.TestCase):
    
    def test_check_author_name_blacklist(self):
        first = check_author_name('University Oslo')
        self.assertEqual(first, False)
        
    def test_check_author_name_single_word(self):
        first = check_author_name('Jr.')
        self.assertEqual(first, False)