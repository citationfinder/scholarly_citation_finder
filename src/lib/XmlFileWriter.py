#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs

class XmlFileWriter:
    
    ENCODING = 'utf-8'
    
    def __init__(self):
        self.output = None
        self.tabbing = ''
    
    def write(self, line):
        self.output.write(line)
        
    def _write_line(self, line):
        self.output.write("%s%s\n" % (self.tabbing, line))
        
    def write_start_tag(self, tag):
        self._write_line("<%s>" % tag)
        self.tabbing += '\t' # add one tab
        
    def write_close_tag(self, tag):
        self.tabbing = self.tabbing[1:] # remove one tab (\t); a tab is one character long        
        self._write_line("</%s>" % (tag))
        
    def write_element(self, tag, value):
        if value:
            self._write_line("<%s>%s</%s>" % (tag, value, tag))
            
    def write_declaration(self):
        self._write_line("<?xml version='1.0' encoding='{}'?>".format(self.ENCODING))        
    
    def open(self, filename):
        try:
            self.output = codecs.open(filename, 'w+', self.ENCODING) # may just 'w'?
            self.tabbing = '' # reset tabbing for new file
        except(IOError) as e:
            raise IOError('Path to file {} not found: {}'.format(filename, e))           

    def close(self):
        self.output.close()