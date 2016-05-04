from scholarly_citation_finder.apps.citation.mag.IsiFieldofstudy import IsiFieldofstudy

class ScfjsonSerializer:
    
    def __init__(self, database):
        self.database = database
        
    def serialze(self, publication, citations=None, isi_fieldofstudy=False):
        
        if self.database == 'mag':
            publication.title = publication.title.title()

        journal_name = None
        if publication.journal_id:
            journal_name = publication.journal.name
            
        if publication.conference_id:
            if publication.conference.name:
                publication.booktitle = publication.conference.name
            else:
                publication.booktitle = publication.conference.short_name
        
        if not publication.type:
            if publication.conference_id:
                publication.type = 'inproceedings'
            if publication.booktitle:
                publication.type = 'incollection'
            else:
                publication.type = 'article'
        
        if publication.volume:
            publication.volume = self.__convert_to_integer(publication.volume)

        if publication.number:
            publication.number = self.__convert_to_integer(publication.number)

        if publication.pages_from:
            publication.pages_from = self.__convert_to_integer(publication.pages_from)

        if publication.pages_to:
            publication.pages_to = self.__convert_to_integer(publication.pages_to)
        
        authors = []
        for item in publication.publicationauthoraffilation_set.all():
            if item.author_id:
                authors.append(item.author.name)
        
        keywords = []        
        for keyword in publication.publicationkeyword_set.all():
            keywords.append(keyword.name)

        result = {'type': publication.type,
                  'title': publication.title,
                  'year': publication.year,
                  'booktitle': publication.booktitle,
                  'journal_name': journal_name,
                  'volumne': publication.volume,
                  'number': publication.number,
                  'pages_from': publication.pages_from,
                  'pages_to': publication.pages_to,
                  'series': publication.series,
                  'publisher': publication.publisher,
                  'isbn': publication.isbn,
                  'doi': publication.doi,
                  'abstract': publication.abstract,
                  'copyright': publication.copyright,
                  'authors': authors,
                  'keywords': keywords,
                  'citations': []}
        
        if isi_fieldofstudy:
            result['isi_fieldofstudy'] = self.__isi_fieldofstudy_mapping(publication)

        if citations:
            for citation in citations:
                result['citations'].append(self.serialze(citation.publication))
        
        return result
    
    def __convert_to_integer(self, value):
        try:
            return int(value)
        except(ValueError):
            return None
        
    def __isi_fieldofstudy_mapping(self, publication):
        # Sort field of study in descending level order, i.e. check first level 1 and then level 0.
        # Don't consider field of studies with a confidence lower then 0.5
        query = publication.publicationfieldofstudy_set.filter(level__gte=0, level__lte=1).order_by('-level', '-confidence')
        # Iterate over all level 1 and 0 field of studies
        for publication_fos in query.iterator():
            if publication_fos.level == 0 and publication_fos.fieldofstudy_name in IsiFieldofstudy.mappingLevel0:
                return IsiFieldofstudy.mappingLevel0[publication_fos.fieldofstudy_name]
            elif publication_fos.level == 1 and publication_fos.fieldofstudy_name in IsiFieldofstudy.mappingLevel1:
                return IsiFieldofstudy.mappingLevel1[publication_fos.fieldofstudy_name]
        return None
