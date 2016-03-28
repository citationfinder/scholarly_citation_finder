from __future__ import absolute_import
from celery import shared_task
import os.path
import logging
import csv
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .evaluation.RandomAuthorSet import RandomAuthorSet
from .CitationFinder import CitationFinder, EmptyPublicationSetException
from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import create_dir
from .CitationFinder2 import CitationFinder2

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
def evaluation_run(name, strategies):
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
    
    :param author_id:
    :param evaluation:
    :raise ObjectDoesNotExits:
    :raise EmptyPublicationSetException: 
    '''
    result = []
    try:
        citationfinder = CitationFinder(database='mag', evaluation=True)
        author_id, length_publication_set = citationfinder.publication_set.set_by_author(id=int(author_id))
        logger.info('{} author: set {} publications'.format(author_id, length_publication_set))
        citationfinder.hack()
        
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


@shared_task
def citations(strategy, type, id=None, name=None, database='mag'):
    '''
    
    :param id:
    :param evaluation:
    :raise ObjectDoesNotExits:
    :raise EmptyPublicationSetException: 
    '''
    try:
        citationfinder = CitationFinder(database=database)
        if type == 'author':
            id, length_publication_set = citationfinder.publication_set.set_by_author(name=name, id=id)
        elif type == 'journal':
            id, length_publication_set = citationfinder.publication_set.set_by_journal(name=name, id=id)
        else:
            raise Exception('Unknown type: {}'.format(type))
        logger.info('{} {}: set {} publications'.format(id, type, length_publication_set))
        
        citationfinder.hack()
        
        strategies_name = citationfinder.run(strategy)
        logger.info('{}: finished strategy "{}"'.format(id, strategies_name))
        citationfinder.store(path=create_dir(os.path.join(config.DOWNLOAD_TMP_DIR, strategies_name)),
                             filename=id)
    except(ObjectDoesNotExist, MultipleObjectsReturned, EmptyPublicationSetException) as e:
        raise e

@shared_task
def citations_cron(limit=None, database='default'):
    citationfinder = CitationFinder2(database=database)
    citationfinder.run(limit=limit)


def __store_evaluation_result(path, filename, row):
    filename = os.path.join(path, 'meta_{}.csv'.format(filename))
    file_exists = os.path.isfile(filename)
    '''
    
    :param filename:
    :param row:
    '''
    try:
        with open(filename, 'a+') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['author_id', 'author_num_citations', 'author_num_publications', 'num_inspected_publications', 'num_citations'])
            writer.writerow(row)
        return filename
    except(IOError) as e:
        raise e
