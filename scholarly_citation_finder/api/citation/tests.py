#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
import os.path

import tasks

class TasksTest(TestCase):
    fixtures = ['sample_data']

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_mag_authors_citations(self):
        author_id = 1
        first = tasks.mag_authors_citations(author_id)
        self.assertTrue(first)
