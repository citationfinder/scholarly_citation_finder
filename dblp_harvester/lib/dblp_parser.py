from lxml import etree
#import os, sys
from unidecode import unidecode
from search_for_citations.models import Publication

"""
https://github.com/Ajeo/dblp-to-csv/blob/master/parser.py
"""
class DblpParser():
    
    DBLP_DIR = 'downloads/dblp/'
    DBLP_FILE_XML = 'dblp.xml'
    
    # Available elements are:   article|inproceedings|proceedings|book|incollection|phdthesis|mastersthesis|www
    # Available tags are:       author|editor|title|booktitle|pages|year|address|journal|volume|number|month|url|ee|cdrom|cite|
    #                           publisher|note|crossref|isbn|series|school|chapter
    COLLABORATIONS = [u'www', u'phdthesis', u'inproceedings', u'incollection', u'proceedings', u'book', u'mastersthesis', u'article']
    
    def __init__(self):   
        context = etree.iterparse(self.DBLP_DIR + self.DBLP_FILE_XML, load_dtd=True, html=True)
        self.fast_iter(context, self.process_element)

    """
    @func: fast_iter
    @param context : iterparsed (chunk of xml) data
    @param func : handler
    @desc: Read xml chunk. After read, clear and delete chunk to release memory.
            Also, replace html encoding to similar ascii code
    """
    def fast_iter(self, context, func,*args, **kwargs):
        #xml categories
        author_array = []
        title = ''
        abstract = ''
        source = ''
    
        #read chunk line by line
        #we focus author and title
        for event, elem in context:
            if elem.tag == 'author':
                author_array.append(unidecode(elem.text))
    
            if elem.tag == 'title':
                if elem.text:
                    title = unidecode(elem.text)
                
            if elem.tag == 'abstract':
                if elem.text:
                    abstract = unidecode(elem.text)

            if elem.tag == 'ee':
                if elem.text:
                    source = unidecode(elem.text)
    
            if elem.tag in self.COLLABORATIONS:
                publication = Publication(
                    title=title,
                    abstract=abstract,
                    source=source,
                    dblp_id=1)
                publication.save()
                
                for author in author_array:
                    publication.authors.create(last_name=author)
                    
                del author_array[:]
     
            # Clear element
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context
        #clear chunks

    #@func: process_element
    #@param elem : parsed data of chunk
    #@param fout : file name to write
    #@desc: It is handler to write content. just write content to file
    def process_element(self, elem, fout):
        print(elem)
        print >>fout, elem
        
DblpParser()