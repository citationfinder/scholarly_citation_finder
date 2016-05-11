from __future__ import absolute_import
from celery import shared_task
import os.path
import logging
import csv
from django.core.exceptions import ObjectDoesNotExist

from .RandomAuthorSet import RandomAuthorSet
from ..CitationFinder import CitationFinder, EmptyPublicationSetException
from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import create_dir

logger = logging.getLogger(__name__)
AUTHOR_SET_FILENAME = 'authors.csv'


@shared_task
def evaluation_create_author_set(name, setsize, num_min_publications, database='mag'): 
    '''
    Task to create a random author set.
    
    :param name: Evaluation name
    :param setsize: Size of the site, i.e. the number of authors
    :param num_min_publications: Minimum number of an author's publications
    :param database: Database name
    '''
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
def evaluation_run(name, strategies):
    '''
    Evaluation run task.
    
    :param name: Evaluation name
    :param strategies: List of strategies
    '''
    evaluation_dir = os.path.join(config.EVALUATION_DIR, name)
    with open(os.path.join(evaluation_dir, AUTHOR_SET_FILENAME)) as author_set_file:
        reader = csv.DictReader(author_set_file)
        for row in reader:
            if len(row) == 3:
                try:
                    strategies_result = evaluation_citations(author_id=row['author_id'], evaluation_name=name, strategies=strategies)
                    for strategy_result in strategies_result:
                        __store_evaluation_result(path=evaluation_dir,
                                                  filename=strategy_result['strategy_name'],
                                                  row=[row['author_id'],
                                                       row['num_citations'],
                                                       row['num_publications'],
                                                       strategy_result['num_inspected_publications'],
                                                       strategy_result['num_citations']])
                except(EmptyPublicationSetException):
                    continue
                except(ObjectDoesNotExist) as e:
                    raise e
    return True


@shared_task
def evaluation_citations(author_id, strategies=None, evaluation_name='default'):
    '''
    Evaluation run view.
    
    :param author_id: Author ID
    :param strategies: List of strategies
    :param evaluation_name: Evaluation name
    :raise ObjectDoesNotExits:
    :raise MultipleObjectsReturned:
    :raise EmptyPublicationSetException: 
    '''
    result = []
    try:
        citationfinder = CitationFinder(database='mag', evaluation=True)
        author_id, length_publication_set = citationfinder.publication_set.set_by_author(id=int(author_id))
        logger.info('{} author: set {} publications'.format(author_id, length_publication_set))
        citationfinder.load_stored_citations()
        
        for strategy in strategies:
            strategy_name = citationfinder.run(strategy)
            logger.info('{}: finished strategy "{}"'.format(author_id, strategy_name))
            num_inspected_publications, num_citations = citationfinder.store_evaluation(path=create_dir(os.path.join(config.EVALUATION_DIR, evaluation_name, strategy_name)),
                                                                                        filename=author_id)
            result.append({'strategy_name': strategy_name,
                           'num_inspected_publications': num_inspected_publications,
                           'num_citations': num_citations})
        return result
    except(ObjectDoesNotExist) as e:
        raise e
    except(EmptyPublicationSetException) as e:
        raise e


def __store_evaluation_result(path, filename, row):
    '''
    Store evaluation result.
    
    :param path: Path
    :param filename: Name of the file
    :param row: Row to append to the file
    '''
    filename = os.path.join(path, 'meta_{}.csv'.format(filename))
    file_exists = os.path.isfile(filename)

    try:
        with open(filename, 'a+') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['author_id', 'author_num_citations', 'author_num_publications', 'num_inspected_publications', 'num_citations'])
            writer.writerow(row)
        return filename
    except(IOError) as e:
        raise e
