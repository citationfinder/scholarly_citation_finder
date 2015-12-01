#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs

class XmlFileWriter:
    
    ENCODING = 'utf-8'
    MAIN_TAG = 'sfc'
    
    def __init__(self):
        self.output = None
        self.tabbing = ''
        
    def _write(self, line):
        self.output.write("%s%s\n" % (self.tabbing, line))
        
    def write_start_tag(self, tag):
        self._write("<%s>" % tag)
        self.tabbing += '\t' # add one tab
        
    def write_close_tag(self, tag):
        self.tabbing = self.tabbing[1:] # remove one tab (\t); a tab is one character long        
        self._write("</%s>" % (tag))
        
    def write_element(self, tag, value):
        if value:
            self._write("<%s>%s</%s>" % (tag, value, tag))
    
    def open(self, filename):
        try:
            self.output = codecs.open(filename, 'w+', self.ENCODING)
            self._write("<?xml version='1.0' encoding='{}'?>".format(self.ENCODING))
            self.write_start_tag(self.MAIN_TAG)
        except(IOError) as e:
            raise IOError('Path to file {} not found: {}'.format(filename, e))        
            
    def close(self):
        self.write_close_tag(self.MAIN_TAG)
        self.output.close()  