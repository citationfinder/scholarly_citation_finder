from __future__ import absolute_import
from celery import shared_task
import os.path
import logging
import csv
from django.core.exceptions import ObjectDoesNotExist

from scholarly_citation_finder.api.citation.evaluation.RandomAuthorSet import RandomAuthorSet
from scholarly_citation_finder.api.citation.CitationFinder import CitationFinder,\
    EmptyPublicationSetException
from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import create_dir
from scholarly_citation_finder.api.citation.strategy.JournalStrategy import JournalStrategy

logger = logging.getLogger(__name__)
AUTHOR_SET_FILENAME = 'authors.csv'


@shared_task
def evaluation_create_author_set(name, setsize, num_min_publications, database='mag'): 
    dir = create_dir(os.path.join(config.EVALUATION_DIR, name))
    author_set = RandomAuthorSet(database=database)
    logger.info('{} -- create random author set of size {}'.format(name, setsize))
    author_set.create(setsize=setsize, num_min_publications=num_min_publications)
    logger.info('{} -- create random author set done'.format(name))
    
    filename_author_set = author_set.store(os.path.join(dir, AUTHOR_SET_FILENAME))
    #for author_info in e.get():
    #    author_id = author_info['author_id']
    #    pass
    return filename_author_set


@shared_task
def evaluation_run(name):
    with open(os.path.join(config.EVALUATION_DIR, name, AUTHOR_SET_FILENAME)) as author_set_file:
        reader = csv.reader(author_set_file)
        next(reader, None)  # skip the headers
        for row in reader:
            if len(row) == 3:
                try:
                    authors_citations(author_id=row[0], evaluation=True, evaluation_name=name)
                except(EmptyPublicationSetException):
                    continue
    return True


@shared_task
def authors_citations(author_id, evaluation=False, evaluation_name=None):
    '''
    
    :param author_id:
    :param evaluation:
    :raise EmptyPublicationSetException: 
    '''
    
    try:
        print(author_id)
        citationfinder = CitationFinder(evaluation=evaluation)
        author_id, length_publication_set = citationfinder.publication_set.set_by_author(id=int(author_id))
        logger.info('set {} publications by author {}'.format(length_publication_set, author_id))
        citationfinder.hack()
        
        logger.info('run')
        #citation_finder.run([AuthorStrategy(ordered=True, recursive=True, min_year=False),
        #                     JournalStrategy(ordered=True, min_year=True)])
        strategies_name = citationfinder.run([JournalStrategy()])
        logger.info('done run strategy: {}'.format(strategies_name))
        if evaluation:
            output_path = create_dir(os.path.join(config.EVALUATION_DIR, evaluation_name, strategies_name))
            citationfinder.store_evaluation(filename=os.path.join(output_path, '{}.csv'.format(author_id)))
        else:
            citationfinder.store()
    except(EmptyPublicationSetException) as e:
        raise e

