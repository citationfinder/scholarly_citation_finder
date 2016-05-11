#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs

class CsvFileWriter:
    '''
    Writer to create a CSV file.
    '''
    
    output = None
        
    def open(self, filename, encoding='utf-8', mode='w+'):
        self.output = codecs.open(filename, mode=mode, encoding=encoding)
        return filename
        
    def close(self):
        self.output.close()
        
    def write_line(self, string):
        self.output.write(string + '\n')
        
    def write_header(self, string):
        self.write_line('# ' + string)
        
    def write_header2(self, *args):
        self.write_header(','.join([str(column) for column in args]))        
    
    def write_values(self, column1, column2):
        self.write_line('{},{}'.format(column1, column2))

    def write_values2(self, *args):
        self.write_line(','.join([str(column) for column in args]))
