#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
from lxml import etree

from ..Harvester import Harvester
from scholarly_citation_finder.api.citation.CsvFileWriter import CsvFileWriter


class DblpHarvester(Harvester):
    
    COLLABORATIONS = [
        'article',
        #'inproceedings',
        'proceedings',
        'book',
        #'incollection',
        'phdthesis',
        'mastersthesis',
        #'www'
    ]

    # Furher avaible tags:  address|month|url|cdrom|cite|note|crossref|school|chapter
    FIELD_MAPPING = {
        'title': 'title',
        'author': 'authors',
        'editor': 'authors',
        'year': 'year',
        'booktitle': 'booktitle',
        'journal': 'journal',
        'volume': 'volume',
        'number': 'number',
        #pages
        'series': 'series',
        'publisher': 'publisher',
        'isbn': 'isbn',
        # doi
        # abstract
        'ee': 'urls'
    }
    
    def __init__(self, **kwargs):
        super(DblpHarvester, self).__init__('dblp', **kwargs)
    
    def harvest(self, filename=None, limit=None):
        '''
        
        :param filename:
        :param limit:
        :return: Number of parsed publications
        '''
        if filename is None:
            filename = os.path.join(self.download_dir, 'dblp.xml')
        if limit:
            self.limit = int(limit)
        else:
            self.limit = None
            

        if os.path.isfile(filename):
            self.start_harevest()
            context = etree.iterparse(filename, load_dtd=True, html=True)
            num_publications = self._fast_iter(context)
            self.stop_harvest()
            return num_publications
        else:
            raise IOError('File {} not found'.format(filename))

    def _fast_iter(self, context):
        '''
        @see: https://github.com/Ajeo/dblp-to-csv/blob/master/parser.py
        @param context : iterparsed (chunk of xml) data
        
        :param context:
        :return: The number of parsed publications
        '''
        cite_writer = CsvFileWriter()
        cite_writer.open(os.path.join(self.download_dir, 'cite.csv'), mode='a+')
        
        publication = {}
        conference_short_name = None
        journal_name = None
        authors = []
        urls = []
        citations = []
        
        #read chunk line by line
        #we focus author and title
        for _, elem in context:
            if elem.tag == 'html' or elem.tag == 'body':
                continue
            # title
            elif elem.tag == 'title' and elem.text:
                title = elem.text
                if title.endswith('.'):
                    title = title[:-1]
                publication[self.FIELD_MAPPING[elem.tag]] = title
            # author and editor
            elif elem.tag in ('author', 'editor') and elem.text:
                field = self.FIELD_MAPPING['author']
                authors.append(elem.text)
            # pages
            elif elem.tag == 'pages' and elem.text:
                pages = elem.text.split('-')
                publication['pages_from'] = pages[0]
                if len(pages) > 1:
                    publication['pages_to'] = pages[1]
            # ee
            elif elem.tag == 'ee' and elem.text:
                field = self.FIELD_MAPPING['ee']
                urls.append(elem.text)

                if 'http://dx.doi.org/' in elem.text:
                    publication['doi'] = elem.text.replace('http://dx.doi.org/', '')
            # crossref
            elif elem.tag == 'crossref' and elem.text:
                conference_short_name = elem.text.split('/')[1] # 'conf/naa/2008' -> 'naa'
            elif elem.tag == 'cite' and elem.text:
                if elem.text != '...':
                    citations.append(elem.text)
            # journal_name
            elif elem.tag == 'journal' and elem.text:
                journal_name = elem.text
            # other
            elif elem.tag in self.FIELD_MAPPING and elem.text:
                publication[self.FIELD_MAPPING[elem.tag]] = elem.text
            elif elem.tag in ('inproceedings', 'incollection', 'www'):
                publication.clear()
                conference_short_name = None
                journal_name = None
                authors = []
                urls = []
                citations = []           
            # collaboration
            elif elem.tag in self.COLLABORATIONS:
                
                publication['type'] = elem.tag
                publication['source'] = 'dbpl:'+elem.get('key')


                # store and clear entry afterwards
                publication_id = self.parse(publication,
                                            conference_short_name=conference_short_name,
                                            journal_name=journal_name,
                                            authors=authors,
                                            urls=urls)
                if publication_id:
                    for citation in citations:
                        cite_writer.write_values(publication_id, citation)
                publication_id = None
                publication.clear()
                conference_short_name = None
                journal_name = None
                authors = []
                urls = []
                citations = []
                
                # Check, if break harvest loop
                if self.check_stop_harvest():
                    break
     
            # Clear element
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context
        # clear chunks
        
        return self.count_publications

#if __name__ == '__main__':
#    harvester = DblpHarvester()
#    harvester.harvest(limit=100000)