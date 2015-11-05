from search_for_citations.models import Publication

def parse_publication(title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, pages=None, abstract=None, doi=None, citeseerx_id=None, source=None):

    if title and authors:

        if date and pages and (booktitle or (journal and volume)):
            publication = Publication(title=title,
                date=date,
                booktitle=booktitle,
                journal=journal,
                volume=volume,
                pages=pages,
                abstract=abstract,
                doi=doi,
                citeseerx_id=citeseerx_id,
                source=source,
            )
            publication.save()
            # 
            for author in authors:
                publication.authors.create(last_name=author)
                
            print('yes')
        else:
            return False 
    else:
        return False
