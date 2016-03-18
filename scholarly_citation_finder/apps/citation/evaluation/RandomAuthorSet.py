import random
import csv
import logging

from scholarly_citation_finder.apps.core.models import Publication, Author, PublicationReference

logger = logging.getLogger(__name__)


class RandomAuthorSet:
    
    def __init__(self, database='mag'):
        self.database = database
        self.random_authors = []
        
    def get(self):
        return self.random_authors

    def create(self, setsize, num_min_publications=0):
        # init
        random_nums = []; # stores random numbers to prevent duplicates
        num_stored_authors = Author.objects.using(self.database).count()
        if num_stored_authors == 0:
            raise Exception('No authors')

        authors = Author.objects.using(self.database).all()        

        while len(random_nums) < setsize:
            logger.info('size random set: {}'.format(len(random_nums)))
            # get a random number between 0 and num_stored_authors-1
            random_num = random.randint(0, num_stored_authors-1)
            if random_num in random_nums:
                if len(random_nums) == num_stored_authors:
                    break
                else:
                    continue
            author = authors[random_num]
            author_publications = Publication.objects.using(self.database).raw('SELECT publication_id AS id FROM core_publicationauthoraffilation WHERE author_id = %s', [author.id])
            author_num_publications = len(list(author_publications))
            if author_num_publications >= num_min_publications:
                author_num_citations = PublicationReference.objects.using(self.database).filter(reference__in=author_publications).count()            
                self.random_authors.append({'author_id': author.id,
                                            'num_publications': author_num_publications,
                                            'num_citations': author_num_citations})
                random_nums.append(random_num)

    def load(self, filename):
        pass
        
    def store(self, filename):
        with open(filename, 'w+') as output_file:
            dict_writer = csv.DictWriter(output_file, self.random_authors[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(self.random_authors)
        return filename

