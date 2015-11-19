#!/usr/bin/python
# -*- coding: utf-8 -*-
from search_for_citations.models import Publication, Author

import logging
logger = logging.getLogger()

def check_author_name(name):
    # block: n.n., S., Jr., A.
    if ' ' in name:
        # block: University, Università, Universität, Université
        if not any(extension in name for extension in ('Universit', 'et al.')):
            return True
    return False

def parse_publication(title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, pages=None, publisher=None, abstract=None, doi=None, citeseerx_id=None, extractor=None, source=None):

    #print('title=%s' % title)

    if title and authors:

        #if date and pages and (booktitle or (journal and volume)):
            publication = Publication(title=title,
                date=date,
                booktitle=booktitle,
                journal=journal,
                volume=volume,
                pages=pages,
                publisher=publisher,
                abstract=abstract,
                doi=doi,
                citeseerx_id=citeseerx_id,
                extractor=extractor,
                source=source,
            )
            publication.save()
            # 
            
            for author in authors:
                if check_author_name(author):
                    a = Author.objects.filter(last_name=author)
                    if a:
                        publication.authors.add(a[0])
                    else:
                        publication.authors.create(last_name=author)
                else:
                    logger.warn("Not an author name: %s" % author)
            return publication
        #else:
            
        #    return False 
    else:
        logger.warn("No title (%s) or authors" % title)
        #print('no title or authors')
        return False
