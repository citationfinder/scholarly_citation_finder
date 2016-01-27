#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs

class CsvFileWriter:
    
    ENCODING = 'utf-8'
    
    def __init__(self, filename):
        try:
            self.output = codecs.open(filename, 'w+', self.ENCODING)  # may just 'w'?
        except(IOError) as e:
            raise IOError('Path to file {} not found: {}'.format(filename, e))

    def close(self):
        self.output.close()
            
    #def write(self, line):
    #    self.output.write(line)
            
    def write_element(self, value = ''): 
        self.output.write('\t%s' % value)
        
    def write_start_line(self, value):
        self.output.write('\n%s' % value)