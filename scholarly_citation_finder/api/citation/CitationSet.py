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
    
    def add(self, citations, num_inspected_publications):
        # add
        for citation in citations:
            if citation not in self.citations:
                self.citations.append(citation)
        # output
        self.num_inspected_publications += num_inspected_publications
        self.writer.write_values(self.num_inspected_publications, len(self.citations))

    