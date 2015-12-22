import os.path
from lxml import etree
import logging
from django.db.utils import IntegrityError
logger = logging.getLogger(__name__)


from search_for_citations.lib.Parser import Parser
from ...core.models import Author, Publication, PublicationReference, PublicationUrl


class Parser:

    PUBLICATION_ATTRIBUTES = Parser.PUBLICATION_ATTRIBUTES

    def store_from_xml_file(self, filelist):
        if os.path.isfile(filelist):
            logger.debug('start')
            context = etree.iterparse(filelist, events=('start', 'end'), html=True)
            self._fast_iter(context)
            logger.debug('end')
        else:
            raise IOError('File {} not found'.format(filelist))

    def parse_author(self, last_name):
        try:
            author = Author.objects.get(last_name=last_name)
        except(Author.DoesNotExist):
            author = Author(last_name=last_name)
            author.save()
        return author
    
    def parse_url(self, url, type=''):
        return PublicationUrl(url=url, type=type)

    def store_publication(self, publication, authors=[], references=[], urls=[]):
        try:
            # TODO: check pub already exists
            publication.save()
            for author in authors:
                publication.authors.add(author)
            # store coauthors
            for author in authors:
                for coauthor in authors:
                    if author.last_name not in coauthor.last_name:
                        author.coauthors.add(coauthor)
            # store references
            for reference in references:
                reference.publication = publication
                reference.save()
            for url in urls:
                url.publication = publication
                url.save()
            return True
        except(IntegrityError) as e:
            logger.warn(str(e))
            return False

    def _fast_iter(self, context):
        publication = Publication()
        publication_references = []
        publication_authors = []
        publication_urls = []

        reference = Publication()
        reference_authors = []

        is_reference = False

        for event, elem in context:

            if event in 'start':
                if elem.tag in 'reference':
                    is_reference = True
                    publication_references.append(PublicationReference())
                continue

            # author
            if elem.tag in 'author' and elem.text:
                if is_reference:
                    reference_authors.append(self.parse_author(elem.text))
                else:
                    publication_authors.append(self.parse_author(elem.text))
            # url
            elif elem.tag in 'url' and elem.text:
                if not is_reference:
                    publication_urls.append(self.parse_url(elem.text, elem.get('type', '')))
            # other
            elif elem.tag in self.PUBLICATION_ATTRIBUTES and elem.text:
                if is_reference:
                    setattr(reference, elem.tag, elem.text)
                else:
                    setattr(publication, elem.tag, elem.text)
            
            # publication
            elif elem.tag in 'publication' and not is_reference:
                self.store_publication(publication, publication_authors, publication_references, publication_urls)
                # Reset
                publication_references = []
                publication_authors = []
                publication_urls = []
                publication = Publication()

            # Beginning of an reference
            elif elem.tag in 'context' and elem.text:
                publication_references[-1].context = elem.text
            elif elem.tag in 'reference':
                if self.store_publication(reference, reference_authors):
                    publication_references[-1].reference = reference
                else:
                    del publication_references[-1]
                # Reset
                is_reference = False
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
