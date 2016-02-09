#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
import os.path

from scholarly_citation_finder import config
from .Parser import Parser
from psycopg2._psycopg import DataError


class ParserTest(TestCase):

    def setUp(self):
        self.parser = Parser('dblp')
        
    def tearDown(self):
        self.parser.conn.close()
        
    def test_parse_author_success(self):
        id = self.parser.parse_author(u'Na éäüö')
        self.assertTrue(id > 0)
        
    def test_parse_author_dataerror(self):
        self.assertRaises(DataError, self.parser.parse_author, 'This is a much too long title yor an author since it is longer then 100 characters and is goes on and one')

    def test_parse_journal_success(self):
        id = self.parser.parse_journal(u'Na éäüö')
        self.assertTrue(id > 0)
        
    def test_parse_publication_success(self):
        id = self.parser.parse_publication(title=u'Na éäüö')
        self.assertTrue(id > 0)
        
    def test_parse(self):
        first = self.parser.parse(publication={'title':u'Title of my paper is éäüö',
                                               'year': 2006},
                                  conference_short_name=u'Conference é Cat'
                                  journal_name=u'Journél üf Example',
                                  authors=['Jonny', 'Kelly'],
                                  keywords=['Web', 'XML'],
                                  urls=['http://example.org', 'http://ex.ample'])
        self.assertTrue(first)

"""        
    def test_parse_publication(self):
        self.parser.open_output_file(self.SAMPLE_XML)
        first = self.parser.parse_publication(title=u'Hey $äüöé', authors=[u'Na éäüö'])
        self.parser.close_output_file()
        self.assertEqual(first, True)
        os.remove(self.SAMPLE_XML)
    
    def test_check_author_name_blacklist(self):
        first = self.parser.check_author_name('University Oslo')
        self.assertEqual(first, False)
        
    def test_check_author_name_single_word(self):
        first = self.parser.check_author_name('Jr.')
        self.assertEqual(first, False)
"""