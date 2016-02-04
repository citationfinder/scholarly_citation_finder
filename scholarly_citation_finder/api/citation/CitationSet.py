#!/usr/bin/python
# -*- coding: utf-8 -*-
from scholarly_citation_finder.api.citation.CsvFileWriter import CsvFileWriter

class CitationSet:

    writer = None    
    citations = None
    num_inspected_publications = None
    
    def __init__(self):
        self.writer = CsvFileWriter()        
    
    def open(self, filename):
        # reset
        self.num_inspected_publications = 0
        self.citations = []
        #
        self.writer.open(filename)
        self.writer.write_values(0, 0)
        return filename
    
    def close(self):
        self.writer.close()
    
    def add(self, publications):
        # add
        for publication in publications:
            if publication not in self.citations:
                self.citations.append(publication)
        # output
        self.num_inspected_publications += len(publications)
        num_citations = len(self.citations)
        self.writer.write_values(self.num_inspected_publications, num_citations)

    