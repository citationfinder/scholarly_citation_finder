#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase

from file import download_file, extract_file
from process import ProcessException

class TestFile(TestCase):

    def test_download_file_success(self):
        file = 'Conferences.zip'
        first = download_file(path='https://academicgraph.blob.core.windows.net/graph-2015-11-06/',
                              file=file,
                              cwd=None)
        self.assertEqual(first, file)
  
    def test_download_file_wrong_path(self):
        self.assertRaises(ProcessException, download_file, 'https://example.org/', 'non.zip')   