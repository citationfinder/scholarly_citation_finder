import os.path
import codecs
from lxml import etree
from core.models import Publication, Citation, Author

class Parser:
    
    PUBLICATION_ATTRIBUTES = [u'title', u'date', u'booktitle', u'journal', u'volume', u'pages', u'number', u'publisher', u'abstract', u'doi', u'citeseerx_id', u'dblp_id', u'extractor', u'source']
    
    def store_from_xml_file(self, filelist):
        if os.path.isfile(filelist):
            #self.input = codecs.open(filelist, "r", "utf-8")
            context = etree.iterparse(filelist)
            self._fast_iter(context)
        else:
            raise IOError('File {} not found'.format(filelist))
        
    def parse_author(self, last_name):
        try:
            author = Author.objects.get(last_name=last_name)
        except(Author.DoesNotExist):
            author = Author(last_name=last_name)
            author.save()
        return author
    
    def store_publication(self, publication, authors = [], citations = []):
        publication.save()
        for author in authors:
            publication.authors.add(author)
        for citation in citations:
            citation.publication = publication
            citation.save()        
        
    def _fast_iter(self, context):
        publication = Publication()
        publication_citations = []
        publication_authors = []

        reference = Publication()
        reference_authors = []

        is_citation = False
        
        for _, elem in context:
            
            if elem.tag in self.PUBLICATION_ATTRIBUTES and elem.text:
                if is_citation:
                    setattr(reference, elem.tag, elem.text)
                else:
                    setattr(publication, elem.tag, elem.text)
            elif elem.tag in 'author' and elem.text:
                if is_citation:
                    reference_authors.append(self.parse_author(elem.text))
                else:
                    publication_authors.append(self.parse_author(elem.text))
            elif elem.tag in 'publication' and not is_citation:
                self.store_publication(publication, publication_authors, publication_citations)
                # Reset
                publication_citations = []
                publication_authors = []
                publication = Publication()                
            
            # Beginning of an citation    
            elif elem.tag in 'context':
                is_citation = True
                publication_citations.append(Citation())
                
                if elem.text:
                    publication_citations[-1].context = elem.text
            elif elem.tag in 'citation':
                is_citation = False
                self.store_publication(reference, reference_authors)
                publication_citations[-1].reference = reference
                # Reset
                reference = Publication()
                reference_authors = []
                
            
"""
import os.path
import codecs, StringIO
from lxml import etree,objectify

from core.models import Publication
from pprint import pprint
class Parser:
    
    def store_from_xml_file(self, filelist):
        if os.path.isfile(filelist):
            input = codecs.open(filelist, "r", "utf-8")
            
            buffer = None
            
            for line in input:

                if line in '<publication>\n':
                    buffer = ''
                elif line in '</publication>\n':
                    buffer += line
                    self.parse_publication(buffer)
                    buffer = None
                    
                if buffer is not None:
                    buffer += line     
        else:
            raise IOError('File {} not found'.format(filelist))
        
    def parse_publication(self, xml_string):
        parser = etree.HTMLParser(encoding='utf-8')
        lookup = objectify.ObjectifyElementClassLookup()
        parser.set_element_class_lookup(lookup)
        pub = objectify.fromstring(xml_string)
        print(objectify.dump(pub))

        publication = Publication()
        
        for attr, value in pub.__dict__.iteritems():
            if attr in 'author':
                pass
            elif attr in 'citation':
                pass
            else:
                publication.


"""