from django.test import TestCase

from .lib.CitationExtractor import CitationExtractor
# Create your tests here.

class ViewsTest(TestCase):
    
    def test_url_not_well_formed(self):
        first = CitationExtractor().url_exits('http://example./paper.pdf')
        self.assertEqual(first, False)    
    
    def test_url_does_not_exits(self):
        first = CitationExtractor().url_exits('http://example.org/paper.pdf')
        self.assertEqual(first, False)
        
    def test_pdf_exits(self):
        first = CitationExtractor().url_exits('http://www.informatik.uni-bremen.de/agra/doc/work/evohot04.pdf')
        self.assertEqual(first, False)