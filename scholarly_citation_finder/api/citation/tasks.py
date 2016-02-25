from __future__ import absolute_import
from celery import shared_task
import os.path
import logging
import csv
from django.core.exceptions import ObjectDoesNotExist

from scholarly_citation_finder.api.citation.evaluation.RandomAuthorSet import RandomAuthorSet
from scholarly_citation_finder.api.citation.CitationFinder import CitationFinder
from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import create_dir
from scholarly_citation_finder.api.citation.strategy.JournalStrategy import JournalStrategy


logger = logging.getLogger(__name__)

@shared_task
def evaluation_create_author_set(name, setsize, num_min_publications, database='mag'): 
    dir = create_dir(os.path.join(config.DOWNLOAD_DIR, 'evaluation', name))
    author_set = RandomAuthorSet(database=database)
    logger.info('{} -- create random author set of size {}'.format(name, setsize))
    author_set.create(setsize=setsize, num_min_publications=num_min_publications)
    logger.info('{} -- create random author set done'.format(name))
    
    filename_author_set = author_set.store(os.path.join(dir, 'authors.csv'))
    #for author_info in e.get():
    #    author_id = author_info['author_id']
    #    pass
    return filename_author_set


@shared_task
def authors_citations(author_id, evaluation=False):
    citationfinder = CitationFinder(evaluation=evaluation)
    try:
        author_id, length_publication_set = citationfinder.publication_set.set_by_author(id=author_id)
        logger.info('set {} publications by author {}'.format(length_publication_set, author_id))
        citationfinder.hack()
        
        logger.info('run')
        #citation_finder.run([AuthorStrategy(ordered=True, recursive=True, min_year=False),
        #                     JournalStrategy(ordered=True, min_year=True)])
        strategies_name, evaluation_result = citationfinder.run([JournalStrategy()])
        logger.info('done run strategy: {}'.format(strategies_name))
        if evaluation:
            output_path = create_dir(os.path.join(config.DOWNLOAD_DIR, 'citationfinder', strategies_name))
            store_evaluation_result_as_csv(evaluation_result,
                                           filename=os.path.join(output_path, '{}.csv'.format(author_id)))
        else:
            citationfinder.store()
    except(ObjectDoesNotExist) as e:
        logger.info(str(e))

def store_evaluation_result_as_csv(evaluation_result, filename):
    with open(filename, 'w+') as csvfile:
        num_inspected_publications = 0
        writer = csv.writer(csvfile)
        writer.writerow([0, 0])
        for result in evaluation_result:
            num_inspected_publications += result[0]
            writer.writerow([num_inspected_publications, result[1]])
