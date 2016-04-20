#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase

from .PublicationDocumentCrawler import PublicationDocumentCrawler


class PublicationDocumentCrawlerTest(TestCase):

    def setUp(self):
        self.crawler = PublicationDocumentCrawler()

    def test_use_html_page_to_find_pdf(self):
        #first = self.crawler.find_pdf_hyperrefs('http://link.springer.com/book/10.1007%2F978-3-642-19357-6')
        #self.assertEqual(first, 'http://link.springer.com/content/pdf/10.1007%2F978-3-642-19357-6.pdf')
        first = self.crawler.__find_document_on_website('http://www.mdpi.com/2224-2708/2/2/172')
        self.assertEqual(first[0], 'http://www.mdpi.com/2224-2708/2/2/172/pdf')
        #first = self.crawler.__find_document_on_website('http://www.computer.org/csdl/proceedings/dcoss/2011/0512/00/05982219-abs.html')
        #self.assertEqual(first, 'http://www.computer.org/csdl/proceedings/dcoss/2011/0512/00/05982219.pdf')

    def test_use_search_engine_to_find_pdf_sucess(self):
        first = self.crawler.get_by_search_engine('kernel completion for learning consensus support vector machines in bandwidth limited sensor networks')
        self.assertEqual(first[0], 'http://www-ai.cs.uni-dortmund.de/PublicPublicationFiles/lee_poelitz_2014a.pdf')
        
        first = self.crawler.get_by_search_engine('advances in cloud and ubiquitous computing')
        self.assertEqual(first[0], 'http://www.ronpub.com/publications/OJCC_2015v2i2n01e_Groppe.pdf')

        #first = self.crawler.get_by_search_engine('kernel completion for learning consensus support vector machines in bandwidth limited sensor networks')
        #self.assertEqual(first[0], 'http://www-ai.cs.uni-dortmund.de/PublicPublicationFiles/lee_poelitz_2014a.pdf')

    def test_use_search_engine_to_find_pdf_failed(self):
        first = self.crawler.get_by_search_engine('Automated composition and execution of hardware-accelerated operator graphs')
        self.assertEqual(first, [])
