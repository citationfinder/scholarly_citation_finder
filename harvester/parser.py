from search_for_citations.models import Publication

def parse_publication(title, abstract, source, citeseerx_id, authors):
    publication = Publication(title=title,
        abstract=abstract,
        source=source,
        citeseerx_id=citeseerx_id
    )
    #publication.save()
        
    #for author in authors:
    #    publication.authors.create(last_name=author)
    return True