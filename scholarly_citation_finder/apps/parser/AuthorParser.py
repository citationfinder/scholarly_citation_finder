#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from django.db.utils import DataError

from scholarly_citation_finder.tools.nameparser.AuthorNameParser import AuthorNameParser
from scholarly_citation_finder.apps.core.models import Author, AuthorNameBlock, AuthorNameVariation
from scholarly_citation_finder.apps.parser.Exceptions import ParserDataError

logger = logging.getLogger(__name__)


class AuthorParser:
    
    def __init__(self, database):
        self.database = database
    
    def parse(self, name):
        author_name = AuthorNameParser(name, normalize=True)
        if author_name.last and author_name.first:
            try:
                # Get block
                block, _ = AuthorNameBlock.objects.using(self.database).get_or_create(name='%s,%s' % (author_name.last, author_name.first[0]))

                # Get or create name variation
                variation, _ = AuthorNameVariation.objects.using(self.database).get_or_create(block_id=block.id,
                                                                                              first=author_name.first,
                                                                                              middle=author_name.middle if author_name.middle else None,
                                                                                              last=author_name.last,
                                                                                              suffix=author_name.suffix if author_name.middle else None,
                                                                                              nickname=author_name.nickname if author_name.nickname else None)
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
                    variation_short, _ = AuthorNameVariation.objects.using(self.database).get_or_create(block_id=block.id,
                                                                                                        first=author_name.first[0],
                                                                                                        middle=middle,
                                                                                                        last=author_name.last) 
                    if variation_short.author_id:
                        author_id = variation_short.author_id
                    else:
                        name.capitalize()
                        author = Author.objects.using(self.database).create(name=name)
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
