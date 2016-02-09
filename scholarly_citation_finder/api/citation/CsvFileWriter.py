#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs

class CsvFileWriter:
    
    output = None
        
    def open(self, filename, encoding='utf-8'):
        self.output = codecs.open(filename, 'w+', encoding=encoding)
        
    def close(self):
        self.output.close()
        
    def write_line(self, string):
        self.output.write(string + '\n')
        
    def write_header(self, string):
        self.write_line('# ' + string)
    
    def write_values(self, column1, column2):
        self.write_line('{}, {}'.format(column1, column2))
