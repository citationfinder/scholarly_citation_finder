from scholarly_citation_finder.apps.core.models import Author, Publication, PublicationReference,\
    Conference, Journal, FieldOfStudy
from django.core.exceptions import ObjectDoesNotExist

class PublicationSet:
    
    publications = None
    publications_idstring = ''
    
    def __init__(self, database='mag'):
        self.database = database
        pass

    def is_set(self):
        return self.publications is not None
    
    def set(self, publications):
        self.publications = publications
        self.publications_idstring = ','.join([publication.id for publication in self.publications])
        return len(self.publications)

    def set_by_author(self, name=None, id=None):
        '''
        
        :param name: Name of the author
        :param id: ID of the author
        :return: Author, if author was found in database otherwise False
        '''
        try:
            query = Author.objects.using(self.database_name)
            if id:
                author = query.get(id=id)
            else:
                author = query.get(name=name)
                
            #author_publication = PublicationAuthorAffilation.objects.using(self.database_name).filter(author=author)
            #Publication.objects.using(self.database_name).filter()
            num_publications = self.set(Publication.objects.using(self.database_name).filter(publicationauthoraffilation__author=author))
            return (author, num_publications)
        except(ObjectDoesNotExist) as e:
            raise e
            
        """    
        self.cursor.execute("SELECT id FROM core_author WHERE name LIKE %s LIMIT 1", (name,))
        result = self.cursor.fetchone()
        
        if result:
            id = result[0]
            self._open_output_file(id)
            self.logger.info('search author "{}", found author id: {}'.format(name, id))
            self.cursor.execute("SELECT publication_id FROM core_publicationauthoraffilation WHERE author_id = %s", (id,))
            self.set_publication_search_set(self._sqllist2array(self.cursor.fetchall()))
            return True
        else:
            self.logger.info('search author "{}", found nothing'.format(name))
        return False     
        """    

    def set_by_journal(self, name=None, id=None):
        pass

    def get_min_publication_year(self, publications_ids):
        pass

    def get_authors(self, ordered=None):
        '''
        Find all authors (precise author IDs) of the given publication search set.
        
        :param publications_ids:
        :return: Array of author IDs ordered descending by frequency
        '''
        #self.cursor.execute("SELECT author_id, COUNT(author_id) as num FROM core_publicationauthoraffilation WHERE publication_id IN "+self._array2sqllist(publication_search_set)+" GROUP BY author_id ORDER BY num DESC")
        #return self._sqllist2array(self.cursor.fetchall())
        
        if ordered:
            return list(Author.objects.using(self.database).raw("SELECT author_id AS id FROM core_publicationauthoraffilation WHERE publication_id IN ("+self.publications_idstring+") GROUP BY author_id ORDER BY num DESC"))
        else:
            return Author.objects.using(self.database).filter(publicationauthoraffilation__publication__in=self.publications).distinct()
        
    def get_conferences(self):
        return Conference.objects.using(self.database).filter(publication__in=self.publications).distinct()

    def get_journals(self):
        '''
        Find all journals (precise journal IDs) of the given publication search set.
        
        :param publications_ids:
        :return: Array of journal IDs ordered descending by frequency
        '''
        #self.cursor.execute("SELECT journal_id, COUNT(journal_id) as num FROM core_publication WHERE publication_id IN "+self._array2sqllist(publication_search_set)+" GROUP BY journal_id ORDER BY num DESC")
        #return self._sqllist2array(self.cursor.fetchall())
        return Journal.objects.using(self.database).filter(publication__in=self.publications).distinct()
    
    def get_fieldofstudies(self):
        return FieldOfStudy.objects.using(self.database_name).filter(publicationkeyword__publication__in=self.publications).distinct()
    
