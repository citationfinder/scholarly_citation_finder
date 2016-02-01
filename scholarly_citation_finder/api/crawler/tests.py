from django.test import TestCase

from .PdfFinder import PdfFinder


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