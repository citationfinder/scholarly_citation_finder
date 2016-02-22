from scholarly_citation_finder.api.Process import Process
from scholarly_citation_finder.apps.core.models import Publication, PublicationAuthorAffilation,\
    Author, PublicationReference
import random
import os.path
from scholarly_citation_finder.lib.CsvFileWriter import CsvFileWriter

class EvaluationAuthorSet(Process):
    
    def __init__(self, name, database='mag'):
        super(EvaluationAuthorSet, self).__init__('evaluation/{}'.format(name))
        self.database = database

    def create_random_author_set(self, set_size):        
        # init
        random_nums = []; # stores random numbers to prevent duplicates
        num_stored_authors = Author.objects.using(self.database).count()
        authors = Author.objects.using(self.database).all()        

        # prepare CSV output
        output = CsvFileWriter()
        output_filename = output.open(os.path.join(self.download_dir, 'authors.csv'))
        output.write_header2('author_id', 'num_publications', 'num_citations')
        
        self.logger.info('{} -- create random author set of size {}, file: {}'.format(self.name, set_size, output_filename))
        
        while len(random_nums) < set_size:
            # get a random number between 0 and num_stored_authors-1
            random_num = random.randint(0, num_stored_authors-1)
            if random_num in random_nums:
                continue
            
            random_nums.append(random_num)
            #
            author = authors[random_num:random_num+1][0]
            author_num_publications, author_num_citations = self.__get_author_statistics(author)
            output.write_values2(author.id, author_num_publications, author_num_citations)
        output.close()
        self.logger.info('{} -- create random author set done'.format(self.name))
            
    def __get_author_statistics(self, author):
        author_publications = Publication.objects.using(self.database).raw('SELECT publication_id AS id FROM core_publicationauthoraffilation WHERE author_id = %s', [author.id])
        author_num_citations = PublicationReference.objects.using(self.database).filter(reference__in=author_publications).count()
        return len(list(author_publications)), author_num_citations
        
            
        