#!/usr/bin/python
# -*- coding: utf-8 -*
from django.test import TestCase
from .Harvester import get_arguments


class HarvesterTest(TestCase):

    def setUp(self):
        #self.harvester = Harvester('test')
        pass

    def test_get_arguments_short_forms(self):
        kwargs = get_arguments(['-l', '20', '-f', '2015-02-01', '-u', '2015-02-28'])
        self.assertEqual(kwargs['limit'], 20)
        self.assertEqual(kwargs['_from'], '2015-02-01')
        self.assertEqual(kwargs['until'], '2015-02-28')

    def test_get_arguments_long_forms(self):
        kwargs = get_arguments(['--limit', '20', '--from', '2015-02-01', '--until', '2015-02-28'])
        self.assertEqual(kwargs['limit'], 20)
        self.assertEqual(kwargs['_from'], '2015-02-01')
        self.assertEqual(kwargs['until'], '2015-02-28')
