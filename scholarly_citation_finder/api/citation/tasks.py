from __future__ import absolute_import
from celery import shared_task
import os.path
import logging
import csv
from django.core.exceptions import ObjectDoesNotExist

from scholarly_citation_finder.api.citation.evaluation import RandomAuthorSet
from scholarly_citation_finder.api.citation.CitationFinder import CitationFinder
from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import create_dir
from scholarly_citation_finder.api.citation.strategy.JournalStrategy import JournalStrategy


logger = logging.getLogger(__name__)
"""
@shared_task
def create_evaluation(name, setsize, num_min_publications):
    dir = create_dir(os.path.join(config.DOWNLOAD_DIR, name))
    e = RandomAuthorSet(name)
    logger.info('{} -- create random author set of size {}'.format(name, setsize))
    e.create(setsize, num_min_publications)
    logger.info('{} -- create random author set done'.format(name))
    
    e.store(path=os.path.join(dir, 'authors.csv'))
    for author_info in e.get():
        author_id = author_info['author_id']
        pass
    return
"""

@shared_task
def authors_citations(author_id, evaluation=False):
    citationfinder = CitationFinder(evaluation=evaluation)
    try:
        author_id, length_publication_set = citationfinder.publication_set.set_by_author(id=author_id)
        logger.info('set {} publications by author {}'.format(length_publication_set, author_id))
        citationfinder.hack()
        
        logger.info('run')
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
