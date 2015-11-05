from django.test import TestCase

from .parser import parse_publication
# Create your tests here.

class ParserTest(TestCase):
    
    def test_insert(self):
        first = parse_publication(
            title='Test Title',
            abstract='Hello world',
            source='my.pdf',
            citeseerx_id='-1',
            authors = ['Author 1']
        )
        self.assertEqual(first, True, 'Test insert a publication')    