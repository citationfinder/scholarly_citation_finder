#!/usr/bin/python
# -*- coding: utf-8 -*-
from scholarly_citation_finder.api.citation.CsvFileWriter import CsvFileWriter

class CitationSet:

    writer = None    
    citations = []
    num_inspected_publications = 0
    
    def open(self, path, name):
        self.writer = CsvFileWriter()        
        filename = self.writer.open(path, name)
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

    