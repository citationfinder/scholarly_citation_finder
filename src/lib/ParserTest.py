#!/usr/bin/python
# -*- coding: utf-8 -*
import unittest
from .Parser import Parser
from config import TEST_PATH

class ParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser('test_parser')
        
    def test_harvest(self):
        self.parser.open_output_file(TEST_PATH+'test_parser.xml')
        first = self.parser.parse_publication(title=u'Hey $äüöé', authors=[u'Na éäüö'])
        self.parser.close_output_file()
        self.assertEqual(first, True)
    
    def test_check_author_name_blacklist(self):
        first = self.parser.check_author_name('University Oslo')
        self.assertEqual(first, False)
        
    def test_check_author_name_single_word(self):
        first = self.parser.check_author_name('Jr.')
        self.assertEqual(first, False)