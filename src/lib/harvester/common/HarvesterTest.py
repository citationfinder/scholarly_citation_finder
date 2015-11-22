#!/usr/bin/python
# -*- coding: utf-8 -*
import unittest
from ..common.Harvester import Harvester

class HarvesterTest(unittest.TestCase):

    def setUp(self):
        self.harvester = Harvester('test_harvester')

    def test_get_arguments_short_forms(self):
        first = self.harvester.get_arguments(['-l', '20'])
        self.assertEqual(first, 20)
        
    def test_get_arguments_long_forms(self):
        first = self.harvester.get_arguments(['--limit', '20'])
        self.assertEqual(first, 20)