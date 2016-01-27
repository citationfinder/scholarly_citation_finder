#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
from django.test import TestCase

from scholarly_citation_finder import config
from .MagNormalize import MagNormalize
from .MagHarvester import MagHarvester

MAG_TEST_DIR = path=os.path.join(config.TEST_DIR, 'harvester', 'mag')

class TestMagNormalize(TestCase):

    def setUp(self):
        self.mag_normalize = MagNormalize(MAG_TEST_DIR)

    def test_run(self):
        self.mag_normalize.run()
        for _, file in MagNormalize.FILES.iteritems():
            output = os.path.join(MAG_TEST_DIR, '{}_pre.txt'.format(file[:-4]))
            first = os.path.isfile(output)
            self.assertEqual(first, True, 'check file exists: {}'.format(output))
            

class TestMagHarvester(TestCase):
    
    def setUp(self):
        self.mag_harvester = MagHarvester()
        self.mag_harvester.download_dir = MAG_TEST_DIR
        
    def test_run(self):
        self.mag_harvester.run()
        for _, file in MagNormalize.FILES.iteritems():
            output = os.path.join(MAG_TEST_DIR, '~{}_pre.txt'.format(file[:-4]))
            first = os.path.isfile(output)
            self.assertEqual(first, True)   
