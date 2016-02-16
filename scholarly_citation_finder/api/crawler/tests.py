from django.test import TestCase

from .PdfFinder import PdfFinder
from Duckduckgo import Duckduckgo

"""
class PdfFinderTest(TestCase):

    def setUp(self):
        self.pdffinder = PdfFinder()

    def test_get_links(self):
        #first = self.crawler.get_links('http://www.sciencedirect.com/science/article/pii/S1477842410000394')
        pass

    def test_find_pdf(self):
        first = self.pdffinder.find_pdf('http://link.springer.com/book/10.1007%2F978-3-642-19357-6')
        self.assertEqual(first, 'http://link.springer.com/content/pdf/10.1007%2F978-3-642-19357-6.pdf')
        first = self.pdffinder.find_pdf('http://www.mdpi.com/2224-2708/2/2/172')
        self.assertEqual(first, 'http://www.mdpi.com/2224-2708/2/2/172/pdf')
        first = self.pdffinder.find_pdf('http://www.computer.org/csdl/proceedings/dcoss/2011/0512/00/05982219-abs.html')
        self.assertEqual(first, 'http://www.computer.org/csdl/proceedings/dcoss/2011/0512/00/05982219.pdf')
"""

class DuckduckgoTest(TestCase):
    
    TEST_KEYWORDS = 'kernel completion for learning consensus support vector machines in bandwidth limited sensor networks'
    
    def setUp(self):
        self.searchengine = Duckduckgo()
        
    def test_query_sucess(self):
        first, _ = self.searchengine.query_publication(self.TEST_KEYWORDS)
        self.assertEqual(first, 'http://www-ai.cs.uni-dortmund.de/PublicPublicationFiles/lee_poelitz_2014a.pdf')
        
        first, _ = self.searchengine.query_publication('advances in cloud and ubiquitous computing')
        self.assertEqual(first, 'http://www.ronpub.com/publications/OJCC_2015v2i2n01e_Groppe.pdf')
        
    def test_query_failed(self):
        first, _ = self.searchengine.query_publication('Automated composition and execution of hardware-accelerated operator graphs')
        self.assertEqual(first, False)
        
        