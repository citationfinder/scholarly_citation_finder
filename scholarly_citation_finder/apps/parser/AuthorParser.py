import logging

from scholarly_citation_finder.tools.nameparser.AuthorNameParser import AuthorNameParser
from .Parser import ParserDataError
from scholarly_citation_finder.apps.core.models import Author,AuthorNameBlock,\
    AuthorNameVariation
from django.db.utils import DataError

logger = logging.getLogger(__name__)


class AuthorParser:
    
    def __init__(self, database):
        self.database = database
    
    def parse(self, name):
        author_name = AuthorNameParser(name, normalize=True)
        if author_name.last and author_name.first:
            try:
                # Get block
                block = AuthorNameBlock.objects.using(self.database).get_or_create(name='{},{}'.format(author_name.last, author_name.first[0]))
                # Get or create name variation
                variation = AuthorNameVariation.objects.using(self.database).get_or_create(block_id=block.id,
                                                                                           first=author_name.first,
                                                                                           middle=author_name.middle,
                                                                                           last=author_name.last,
                                                                                           suffix=author_name.suffix,
                                                                                           nickname=author_name.nickname)
                if variation.author_id:
                    author_id = variation.author_id
                    #middle = author_name.middle[0] if author_name.middle else None
                    #AuthorNameVariation.objects.using(self.database).get_or_create(block_id=block.id,
                    #                                                               author_id=author_id,
                    #                                                               first=author_name.first[0],
                    #                                                               middle=middle,
                    #                                                               last=author_name.last) 
                else:
                    middle = author_name.middle[0] if author_name.middle else None
                    variation_short = AuthorNameVariation.objects.using(self.database).get_or_create(block_id=block.id,
                                                                                                     first=author_name.first[0],
                                                                                                     middle=middle,
                                                                                                     last=author_name.last) 
                    if variation_short.author_id:
                        author_id = variation_short.author_id
                    else:
                        author = Author.objects.using(self.database).create(name=name.capitalize())
                        author_id = author.id
                        variation_short.author_id = author_id
                        variation_short.save()

                    variation.author_id = author_id
                    variation.save()        
                return author_id
            except(DataError) as e:
                raise ParserDataError('Author name is invalid: %s' % str(e))
        else:
            raise ParserDataError('Author name has no last or first name: %s' % name)
