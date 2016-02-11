#!/usr/bin/python
# -*- coding: utf-8 -*-
from scholarly_citation_finder.api.citation.CsvFileWriter import CsvFileWriter

class CitationSet:

    # PublicationReference
    citations = []
    writer = None
    num_inspected_publications = 0
    
    def __init__(self, publication_set):
        self.publication_set = publication_set
        self.writer = CsvFileWriter()
    
    def __len__(self):
        return len(self.citations)
    
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
        '''
        
        :param citations: PublicationReference
        :param num_inspected_publications:
        '''
        
        # add
        for citation in citations:
            if citation not in self.citations:
                self.citations.append(citation)
                self.publication_set.add(citation.publication_id)

        # output
        self.num_inspected_publications += num_inspected_publications
        self.writer.write_values(self.num_inspected_publications, len(self.citations))
        
    def get(self):
        return self.citations

    