#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import logging
import csv
from lxml import etree
from django.core.exceptions import ObjectDoesNotExist

from scholarly_citation_finder.tools.harvester.Harvester import Harvester
from scholarly_citation_finder.lib.CsvFileWriter import CsvFileWriter
from scholarly_citation_finder.apps.core.models import Publication, PublicationReference
from scholarly_citation_finder.tools.harvester.dblp.DblpDownloader import DblpDownloader
from scholarly_citation_finder.lib.file import DownloadFailedException,\
    UnzipFailedException

logger = logging.getLogger(__name__)


class DblpHarvester(Harvester):
    '''
    Harvester for DBLP database.
    '''
    
    NAME = 'dblp'
    FILENAME_CITE = 'cite.csv'
    
    COLLABORATIONS = [
        'article',
        'inproceedings',
        #'proceedings',
        'book',
        'incollection',
        'phdthesis',
        'mastersthesis',
        #'www'
    ]

    # List of HTML elements which a title can contain
    HTML_ELEMENTS = ['i', 'sub', 'sup', 'tt']

    # Further available tags:  address|month|url|cdrom|note|crossref|school|chapter
    FIELD_MAPPING = {
        #'title': 'title',
        #'author': 'authors',
        #'editor': 'authors',
        'year': 'year',
        'booktitle': 'booktitle',
        'journal': 'journal',
        'volume': 'volume',
        'number': 'number',
        # 'pages': 
        'series': 'series',
        'publisher': 'publisher',
        'isbn': 'isbn',
        # 'doi':
        # 'abstract'
        # 'ee': 'urls'
        # 'cite':
    }
    
    def __init__(self, **kwargs):
        '''
        Create object.
        '''
        super(DblpHarvester, self).__init__(name=self.NAME, **kwargs)

    def download_database(self):
        '''
        Download the database from DBLP.
        '''
        try:
            downloader = DblpDownloader(self.download_dir)
            result = downloader.download()
            if result:
                logger.info('Downloaded and unzipped XML database: {}'.format(result))
            else:
                logger.info('No new data is available')
        except(DownloadFailedException, UnzipFailedException) as e:
            raise e
    
    def harvest(self, filename=None, limit=None, _from=None):
        '''
        Harvest, i.e. collect meta data from the downloaded XML file.
        
        :param filename: DBLP XML file name
        :param limit: Number of maximum publications to parse
        :param _from: Last stored (!) DBLP key, e.g. 'journals/jlp/Winter08'
        :return: Number of parsed publications
        '''
        if filename is None:
            filename = os.path.join(self.download_dir, 'dblp.xml')
        self.set_limit(limit)

        if os.path.isfile(filename):
            self.start_harevest(logger_string='limit={}, from={}'.format(limit, _from))
            num_publications = self._fast_iter(filename, _from=_from)
            self.stop_harvest()
            return num_publications
        else:
            raise IOError('File {} not found'.format(filename))

    def _fast_iter(self, filename, _from=None):
        '''
        Fast iter the XML file.
        
        @see: https://github.com/Ajeo/dblp-to-csv/blob/master/parser.py

        :param filename:
        :param _from: Last stored (!) DBLP key, e.g. 'journals/jlp/Winter08'
        :return: The number of parsed publications
        '''
        cite_writer = CsvFileWriter()
        cite_writer.open(os.path.join(self.download_dir, self.FILENAME_CITE), mode='a+')
        
        publication = {}
        conference_short_name = None
        journal_name = None
        authors = []
        urls = []
        citations = []
        
        context = etree.iterparse(filename, load_dtd=True, html=False)
        for _, elem in context:
            #if elem.tag in ('html', 'body'):
            #    continue

            # collaboration
            if elem.tag in self.COLLABORATIONS:
                key = elem.get('key')
                if _from is not None:
                    # Stop skipping, if the key was found
                    if _from == key:
                        _from = None
                else:
                    publication['type'] = elem.tag
                    publication['source'] = 'dbpl:'+key
    
                    if conference_short_name and 'booktitle' in publication:
                        del publication['booktitle']

                    # store and clear entry afterwards
                    publication_id = self.parser.parse(publication,
                                                       conference={'short_name': conference_short_name},
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
                    
                    # http://pranavk.github.io/python/parsing-xml-efficiently-with-python/
                    #
                    # Check, if break harvest loop
                    if self.check_stop_harvest():
                        break
                del key
            # If from is not None, skip all these steps
            elif _from is None:
                # title
                if elem.tag == 'title' and elem.text:
                    publication['title'] = etree.tostring(elem, method='text', encoding='utf-8').rstrip().rstrip('.')
                # author and editor
                elif elem.tag in ('author', 'editor') and elem.text:
                    try:
                        split = elem.text.rsplit(' ', 1)
                        int(split[1])
                        # some authors have a 0001, 0002, ... at the end, when the name already exists
                        elem.text = '%s (%s)' % (split[0], split[1])
                    except(ValueError, IndexError):
                        pass
                    authors.append(elem.text)
                # pages
                elif elem.tag == 'pages' and elem.text:
                    pages = elem.text.split('-')
                    publication['pages_from'] = pages[0]
                    if len(pages) > 1:
                        publication['pages_to'] = pages[1]
                    del pages
                # ee
                elif elem.tag == 'ee' and elem.text:
                    # doi
                    if 'http://dx.doi.org/' in elem.text:
                        publication['doi'] = elem.text.replace('http://dx.doi.org/', '')
                    # url
                    else:
                        urls.append(elem.text)
                # crossref
                elif elem.tag == 'crossref' and elem.text:
                    split = elem.text.split('/')
                    if len(split) > 2 and split[0] == 'conf':
                        conference_short_name = split[1] # 'conf/naa/2008' -> 'naa'
                    del split
                elif elem.tag == 'cite' and elem.text:
                    if elem.text != '...':
                        citations.append(elem.text)
                # journal_name
                elif elem.tag == 'journal' and elem.text:
                    journal_name = elem.text
                # other
                elif elem.tag in self.FIELD_MAPPING and elem.text:
                    publication[self.FIELD_MAPPING[elem.tag]] = elem.text
                #
                elif elem.tag in ('proceedings', 'www'):
                    publication.clear()
                    conference_short_name = None
                    journal_name = None
                    authors = []
                    urls = []
                    citations = []
                elif elem.text:
                    if elem.tag in self.HTML_ELEMENTS:
                        pass
                    elif elem.tag in ('address', 'month', 'url', 'cdrom', 'note', 'crossref', 'school', 'chapter'):
                        pass
                    else:
                        logger.info('Unknown tag <%s> with value: %s' % (elem.tag, elem.text))

            # Clear element
            if elem.tag not in self.HTML_ELEMENTS: # We stil need the html elements to get the full title
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        # clear chunks
        
        cite_writer.close()
        return self.parser.count_publications
    
    def parse_citations(self):
        try:
            filename = os.path.join(self.download_dir, self.FILENAME_CITE)
            with open(filename) as input:
                reader = csv.reader(input)
                for line in reader:
                    if len(line) == 2:
                        self.__parse_citation(int(line[0]), line[1])
        except(IOError) as e:
            raise e
        
    def __parse_citation(self, publication_id, reference_dblp_key):
        try:
            reference = Publication.objects.using(self.parser.database).get(source='{}:{}'.format(self.NAME, reference_dblp_key))
            PublicationReference.objects.using(self.parser.database).get_or_create(publication_id=publication_id,
                                                                                   reference=reference)
        except(ObjectDoesNotExist) as e:
            logger.info('{},{} - {}'.format(publication_id, reference_dblp_key, str(e)))
