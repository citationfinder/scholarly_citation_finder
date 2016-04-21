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
        name = AuthorNameParser(name, normalize=True)
        if name.title and not name.first:
            name.first = name.title
            #name.title = ''
        name_middle = name.middle if name.middle else None
        name_suffix = name.suffix if name.suffix else None
        name_nickname = name.nickname if name.nickname else None

        if name.last and name.first:
            try:
                # Get block
                block, _ = AuthorNameBlock.objects.using(self.database).get_or_create(name='%s,%s' % (name.last, name.first[0]))

                # Get or create name variation
                variation = AuthorNameVariation.objects.using(self.database).filter(block_id=block.id,
                                                                                    first=name.first,
                                                                                    middle=name_middle,
                                                                                    last=name.last,
                                                                                    suffix=name_suffix,
                                                                                    nickname=name_nickname)[:1]
                if variation:
                    return variation[0].author_id
                else:
                    variation_short = AuthorNameVariation.objects.using(self.database).filter(block_id=block.id,
                                                                                              first=name.first[0],
                                                                                              middle=name_middle[0] if name_middle else None,
                                                                                              last=name.last)[:1]
                    if variation_short:
                        author_id = variation_short[0].author_id
                    else:
                        #name.capitalize()
                        author = Author.objects.using(self.database).create(name=str(name).title())
                        author_id = author.id
                        if len(name.first) > 1: # Otherwise this version was already stored above
                            self.__store_shortname_variation(block.id, author_id, name.first, name_middle, name.last)

                    AuthorNameVariation.objects.using(self.database).create(block_id=block.id,
                                                                            author_id=author_id,
                                                                            first=name.first,
                                                                            middle=name_middle,
                                                                            last=name.last,
                                                                            suffix=name_suffix,
                                                                            nickname=name_nickname)
                    return author_id
            except(DataError) as e:
                raise ParserDataError('Author name is invalid: %s' % str(e))
        else:
            raise ParserDataError('Author name has no last or first name: %s' % name)

    def __store_shortname_variation(self, block_id, author_id, first, middle, last):
        middle = middle[0] if middle else None
        AuthorNameVariation.objects.using(self.database).get_or_create(block_id=block_id,
                                                                       author_id=author_id,
                                                                       first=first[0],
                                                                       middle=middle,
                                                                       last=last)