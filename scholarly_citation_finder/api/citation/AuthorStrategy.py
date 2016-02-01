from CitationFinder import CitationFinder

class AuthorStrategy(CitationFinder):


    def __init__(self):
        super(AuthorStrategy, self).__init__(name='author_strategy')
        
    def run(self, publication_limit=None, time_limit=None):
        super(AuthorStrategy, self).run(publication_limit=publication_limit, time_limit=time_limit)
        #CitationFinder.run(self, publication_limit=publication_limit, time_limit=time_limit)
        publications_authors = self.__find_authors(self.publication_ids)
        self.logger.info('found {} author(s): {}'.format(len(publications_authors), publications_authors))
        self.output.write('# {} for author id\n'.format(self.name))
        for author_id in publications_authors:
            p = self.__find_authors_publications(author_id)
            self.logger.info('Found {} publications of author with id {}'.format(len(p), author_id))
            c = self.__find_citations_in_authors_publications(self.publication_ids, p)
            self.logger.info('{} of these publications cites one they publications of the search set'.format(len(c)))
            self.output.write('{}, {}\n'.format(len(p), len(c)))
        self.output.close()
            
    def __find_min_publication_year(self, publications_ids):
        pass

    def __find_authors(self, publications_ids):
        self.cursor.execute("SELECT author_id, COUNT(author_id) as num FROM core_publicationauthoraffilation WHERE publication_id IN "+self._array2sqllist(publications_ids)+" GROUP BY author_id ORDER BY num DESC")
        return self._sqllist2array(self.cursor.fetchall())
    
    def __find_authors_publications(self, author_id, publications_authors=None):
        #self.cursor.execute("SELECT author_id, COUNT(author_id) as num FROM core_publicationauthoraffilation LEFT JOIN publicationreference ON publicationreference.publication_id =  WHERE publication_id IN %s GROUP BY author_id ORDER BY num DESC", (publications_authors,))
        #return self.cursor.fetchall()

        self.cursor.execute("SELECT publication_id FROM core_publicationauthoraffilation WHERE author_id = %s", (author_id,))
        return self._sqllist2array(self.cursor.fetchall())
    
    def __find_citations_in_authors_publications(self, publications_ids, authors_publications):
        self.cursor.execute("SELECT publication_id as num FROM core_publicationreference WHERE publication_id IN "+self._array2sqllist(authors_publications)+" and reference_id IN "+self._array2sqllist(publications_ids))
        return self._sqllist2array(self.cursor.fetchall())