#!/usr/bin/python
# -*- coding: utf-8 -*-
from scholarly_citation_finder.api.citation.CsvFileWriter import CsvFileWriter
from scholarly_citation_finder.api.citation.PublicationSet import PublicationSet

class CitationSet(PublicationSet):

    writer = None
    num_inspected_publications = 0
    
    def __init__(self, **kwargs):
        super(CitationSet, self).__init__(kwargs)
        self.writer = CsvFileWriter()
    
    def open(self, filename):
        # reset
        self.num_inspected_publications = 0
        self.publications = []
        #
        self.writer.open(filename)
        self.writer.write_values(0, 0)
        return filename
    
    def close(self):
        self.writer.close()
    
    def add(self, citations, num_inspected_publications):
        # add
        for citation in citations:
            if citation not in self.publications:
                PublicationSet.add(self, citation)
        # output
        self.num_inspected_publications += num_inspected_publications
        self.writer.write_values(self.num_inspected_publications, len(self.publications))

    