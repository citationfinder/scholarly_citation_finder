#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path

class CsvFileWriter:
    
    def __init__(self):
        self.num_total_inspected_publications = 0
        self.output = None
        
    def open(self, path, name):
        filename = os.path.join(path, '{}.csv'.format(name))
        self.output = open(filename, 'w+')
        return filename
        
    def close(self):
        self.output.close()
        
    def write_line(self, string):
        self.output.write(string + '\n')
        
    def write_header(self, string):
        self.write_line('# ' + string)
    
    def write_values(self, column1, column2):
        self.write_line('{}, {}'.format(column1, column2))
