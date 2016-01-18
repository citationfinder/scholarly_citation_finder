#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
from django.test import TestCase

from scholarly_citation_finder import config
from .normalize_files import MagNormalize

class TestMagNormalize(TestCase):


    def setUp(self):
        self.mag_normalize = MagNormalize(path=os.path.join(config.TEST_DIR, 'harvester', 'mag'))

    def test_run(self):
        self.mag_normalize.run()
        for _, file in MagNormalize.FILES.iteritems():
            output = os.path.join(config.TEST_DIR, 'harvester', 'mag', '{}_pre.txt'.format(file[:-4]))
            first = os.path.isfile(output)
            self.assertEqual(first, True)