#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
import os.path

import tasks

class TaskTest(TestCase):
    fixtures = ['sample_data']

    TMP_FILE = 'tmp'

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
     
    def test_evaluation_create_author_set(self):
        filename = tasks.evaluation_create_author_set(self.TMP_FILE, 3, 0, 'default')
        first = os.path.isfile(filename)
        self.assertTrue(first)
        if first:
            os.remove(filename)