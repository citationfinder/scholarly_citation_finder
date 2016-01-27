#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
from django.db.utils import DataError

from scholarly_citation_finder import config
from Process import Process
from scholarly_citation_finder.apps.core.models import Author, Journal, Publication


class Parser(Process):
    
    PUBLICATION_ATTRIBUTES = [
        'type',
        'title',
        'date',
        'booktitle'
        'journal',
        'volume',
        'number',
        'pages_from',
        'pages_to',
        'series',
        'publisher',
        'isbn',
        'doi',
        'abstract',
        'copyright',
        'citeseerx_id',
        'dblp_id',
        'arxiv_id',
        'extractor'
    ]

    def __init__(self, name):
        super(Parser, self).__init__(name)
        self.count_publications = 0
        #self.count_citations = 0
        self.logger.info('start -------------------')

    def stop_harvest(self):
        self.logger.info('stop')
  
    #def parse_publication_reference(self, context=None, type=None, title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, number=None, pages=None, publisher=None, abstract=None, doi=None, citeseerx_id=None, dblp_id=None, arxiv_id=None, extractor=None, source=None):
    #    self.count_citations += 1
    #    
    #    self.xml_writer.write_start_tag('reference')
    #    self.xml_writer.write_element('context', context, is_cdata=True)
    #    self.parse_publication(type, title, authors, date, booktitle, journal, volume, number, pages, publisher, abstract, doi, citeseerx_id, dblp_id, arxiv_id, extractor, source)
    #    self.xml_writer.write_close_tag('reference')

    #def _parse_publication_urls(self, urls):
    #    for url in urls:
    #        if isinstance(url, dict):
    #            self.xml_writer._write_line('<%s type="%s">%s</%s>' % ('url', url['type'], url['value'], 'url'))
    #        else:
    #            self.xml_writer.write_element('url', url)

    def check_stop_harvest(self):
        return self.limit and self.count_publications >= self.limit

    def parse_author(self, name):
        try:
            author = Author.objects.using(self.name).get(name=name)
        except(Author.DoesNotExist):
            author = Author(name=name)
            author.save()
        return author
    
    def parse_journal(self, name):
        try:
            journal = Journal.objects.using(self.name).get(name=name)
        except(Journal.DoesNotExist):
            journal = Journal(name=name)
            journal.save()
        return journal        

    def parse_publication(self, entry, check_author=True):
        self.count_publications += 1
        try:
            publication = Publication()
            
            for field in self.PUBLICATION_ATTRIBUTES:
                if field in entry:
                    setattr(publication, field, entry[field])
            
            publication.save(using=self.name)     
            
            if 'authors' in entry:
                for author in entry['authors']:
                    publication.authors.add(self.parse_author(author))
            #if 'keywords' in entry:
            #    for keyword in entry['keywords']:
            #        publication.ke
            #        self.xml_writer.write_element('keyword', keyword)
            if 'urls' in entry:
                for url in entry['urls']:
                    if isinstance(url, dict):
                        url_value = url.value
                        url_type = url.type
                    else:
                        url_value = url
                        url_type = ''
                    publication.publicationurl_set.create(url=url_value, type=url_type)
        except(DataError) as e:
            self.logger.warn(str(e))
        
        return True
    
    
    """
        def check_author_name(self, name):
        try:
            # Milena Mihail, et al.
            name = name.strip().replace(', et al.', '')
            # block: n.n., S., Jr., A.
            if ' ' in name:
                # block: University, Università, Universität, Université
                if not any(extension in name for extension in ('Universit', 'et al.')):
                    return name
        except(AttributeError) as e:
            self.logger.warn(str(e))

        return False
    
    def _check_publication_is_valid(self, entry):
        return 'title' in entry and 'authors' in entry
    
    def parse_publication(self, type=None, title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, number=None, pages=None, publisher=None, abstract=None, doi=None, citeseerx_id=None, dblp_id=None, arxiv_id=None, extractor=None, source=None):
    
        if title and authors:

            self.count_publications += 1
                
            #if date and pages and (booktitle or (journal and volume)):
            self.xml_writer.write_start_tag('publication')
            self.xml_writer.write_element('type', type)
            self.xml_writer.write_element('title', title)
            self.xml_writer.write_element('date', date)
            self.xml_writer.write_element('booktitle', booktitle)
            self.xml_writer.write_element('journal', journal)
            self.xml_writer.write_element('volume', volume)
            self.xml_writer.write_element('pages', pages)
            self.xml_writer.write_element('number', number)
            self.xml_writer.write_element('publisher', publisher)
            self.xml_writer.write_element('abstract', abstract, is_cdata=True)
            self.xml_writer.write_element('doi', doi)
            self.xml_writer.write_element('citeseerx_id', citeseerx_id)
            self.xml_writer.write_element('dblp_id', dblp_id)
            self.xml_writer.write_element('arxiv_id', arxiv_id)
            self.xml_writer.write_element('extractor', extractor)
            self.xml_writer.write_element('source', source)

            for author in authors:
                author = self.check_author_name(author)
                if author:
                    self.xml_writer.write_element('author', author)
                else:
                    self.logger.warn('Not an author name: %s' % author)
            
            self.xml_writer.write_close_tag('publication')
            return True
        else:
            self.logger.warn('No title (%s) or authors' % title)
            #print('no title or authors')
            return False
    """