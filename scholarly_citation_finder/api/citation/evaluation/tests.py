#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
import os.path

from scholarly_citation_finder import config
from scholarly_citation_finder.api.citation.evaluation.EvaluationAuthorSet import EvaluationAuthorSet

"""
class EvaluationAuthorSetTest(TestCase):

    def setUp(self):
        self.author_set = EvaluationAuthorSet('run_a')
        
    def test_run(self):
        self.author_set.run(2)
        first = os.path.isfile(os.path.join(self.author_set.download_dir, 'authors.csv'))
        self.assertTrue(first)
"""