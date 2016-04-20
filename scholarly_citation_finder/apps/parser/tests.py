#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase

from .Parser import Parser
from scholarly_citation_finder.apps.parser.Exceptions import ParserDataError


class ParserTest(TestCase):

    def setUp(self):
        self.parser = Parser('default')
        
    def tearDown(self):
        #self.parser.conn.close()
        pass
        
    def test_parse_author_success(self):
        id = self.parser.parse_author(u'Na éäüö')
        self.assertTrue(id > 0)
        
    def test_parse_author_dataerror(self):
        self.assertRaises(ParserDataError, self.parser.parse_author, 'This is a much too long title yor an author since it is longer then 100 characters and is goes on and one')

    def test_parse_journal_success(self):
        id = self.parser.parse_journal(u'Na éäüö')
        self.assertTrue(id > 0)
        
    def test_parse_publication_success(self):
        id = self.parser.parse_publication(title=u'Na éäüö')
        self.assertTrue(id > 0)
        
    def test_parse(self):
        first = self.parser.parse(publication={'title':u'Title of my paper is éäüö',
                                               'year': 2006},
                                  conference={'short_name': u'Conference é Cat'},
                                  journal_name=u'Journél üf Example',
                                  authors=['Jelly Jonny', 'Key Kelly'],
                                  keywords=['Web', 'XML'],
                                  urls=['http://example.org', 'http://ex.ample'])
        self.assertTrue(first)
