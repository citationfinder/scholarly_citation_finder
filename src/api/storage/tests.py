#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os.path
from django.test import TestCase

from .Parser import Parser
import config
from core.models import Publication, Citation, Author

class ParserTest(TestCase):
    
    XML_FILELIST = os.path.join(config.TEST_DIR, 'harvester', 'citeseerx', 'publication-0.xml.tmp')
    
    def setUp(self):
        self.parser = Parser()
    
        
    def test_store_from_xml_file(self):
        self.parser.store_from_xml_file(self.XML_FILELIST)
        self.assertEqual(Publication.objects.all().count(), 4)
        self.assertEqual(Citation.objects.all().count(), 2)
        self.assertEqual(Author.objects.all().count(), 13)
     
    """
    def test_parse_publication(self):
        xmL_string = '''
        <publication>
    <title>Example Publication</title>
    <date>1999</date>
    <citeseerx_id>10.1.1.1.1484</citeseerx_id>
    <author>J. Körmendy-rácz</author>
    <author>S. Szabó</author>
    <source>http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.1.1484&amp;rep=rep1&amp;type=pdf</source>
     </publication>
    '''
        first = self.parser.parse_publication(xmL_string)
    """