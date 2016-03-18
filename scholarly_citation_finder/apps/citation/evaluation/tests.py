#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
import os.path

from RandomAuthorSet import RandomAuthorSet
from scholarly_citation_finder.apps.core.models import PublicationAuthorAffilation


class RandomAuthorSetTest(TestCase):
    fixtures = ['sample_data']

    TMP_FILE = 'tmp'

    def setUp(self):
        self.author_set = RandomAuthorSet(database='default')
        
    def tearDown(self):
        if os.path.isfile(self.TMP_FILE):
            os.remove(self.TMP_FILE)
     
    def test_create_setsize(self):
        setsize = 3
        
        self.author_set.random_authors = []
        self.author_set.create(setsize)     
        first = len(self.author_set.get())
        self.assertEqual(first, setsize)

    def test_create_num_min_publications(self):
        num_min_publications = 4
        
        self.author_set.random_authors = []
        self.author_set.create(1, num_min_publications)
        author_id = self.author_set.get()[0]['author_id']
        first = PublicationAuthorAffilation.objects.using(self.author_set.database).filter(author_id=author_id).count()
        self.assertGreaterEqual(first, num_min_publications)
 
    def test_store(self):
        self.author_set.random_authors = []
        self.author_set.create(3)
        self.author_set.store(self.TMP_FILE)
        self.assertTrue(os.path.isfile(self.TMP_FILE))
