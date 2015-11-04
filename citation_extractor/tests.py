from django.test import TestCase

from .views import url_exits
# Create your tests here.

class ViewsTest(TestCase):
    
    def test_url_not_well_formed(self):
        first = url_exits('http://example./paper.pdf')
        self.assertEqual(first, False)    
    
    def test_url_does_not_exits(self):
        first = url_exits('http://example.org/paper.pdf')
        self.assertEqual(first, False)