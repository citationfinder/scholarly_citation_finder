#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase

from .PublicationDocumentCrawler import PublicationDocumentCrawler
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

class PublicationDocumentCrawlerTest(TestCase):

    def setUp(self):
        self.crawler = PublicationDocumentCrawler()

    def test_use_html_page_to_find_pdf(self):
        #first = self.crawler.find_pdf_hyperrefs('http://link.springer.com/book/10.1007%2F978-3-642-19357-6')
        #self.assertEqual(first, 'http://link.springer.com/content/pdf/10.1007%2F978-3-642-19357-6.pdf')
        first = self.crawler.use_html_page_to_find_pdf('http://www.mdpi.com/2224-2708/2/2/172')
        self.assertEqual(first[0], 'http://www.mdpi.com/2224-2708/2/2/172/pdf')
        #first = self.crawler.use_html_page_to_find_pdf('http://www.computer.org/csdl/proceedings/dcoss/2011/0512/00/05982219-abs.html')
        #self.assertEqual(first, 'http://www.computer.org/csdl/proceedings/dcoss/2011/0512/00/05982219.pdf')

    def test_use_search_engine_to_find_pdf_sucess(self):
        first = self.crawler.by_search_engine('kernel completion for learning consensus support vector machines in bandwidth limited sensor networks')
        self.assertEqual(first[0], 'http://www-ai.cs.uni-dortmund.de/PublicPublicationFiles/lee_poelitz_2014a.pdf')
        
        first = self.crawler.by_search_engine('advances in cloud and ubiquitous computing')
        self.assertEqual(first[0], 'http://www.ronpub.com/publications/OJCC_2015v2i2n01e_Groppe.pdf')

        #first = self.crawler.by_search_engine('kernel completion for learning consensus support vector machines in bandwidth limited sensor networks')
        #self.assertEqual(first[0], 'http://www-ai.cs.uni-dortmund.de/PublicPublicationFiles/lee_poelitz_2014a.pdf')

    def test_use_search_engine_to_find_pdf_failed(self):
        first = self.crawler.by_search_engine('Automated composition and execution of hardware-accelerated operator graphs')
        self.assertEqual(first, [])
