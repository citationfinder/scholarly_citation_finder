from search_for_citations.models import Publication

def parse_publication(title=None, abstract=None, source=None, citeseerx_id=None, authors=None):
    publication = Publication(title=title,
        abstract=abstract,
        source=source,
        citeseerx_id=citeseerx_id
    )
    publication.save()
    
    for author in authors:
        publication.authors.create(last_name=author)

    return True