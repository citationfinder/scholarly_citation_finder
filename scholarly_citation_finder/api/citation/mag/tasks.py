from __future__ import absolute_import
from celery import shared_task
import os.path
import logging
from django.core.exceptions import ObjectDoesNotExist

from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import create_dir
from scholarly_citation_finder.api.citation.CitationFinder import CitationFinder

logger = logging.getLogger(__name__)


@shared_task
def citations(author_name, author_id):
    try:
        citationfinder = CitationFinder()
        author_id, length_publication_set = citationfinder.publication_set.set_by_author(name=author_name, id=author_id)
        logger.info('set {} publications by author {}'.format(length_publication_set, author_id))
        citationfinder.hack()
        citationfinder.citations = citationfinder.citing_papers
    
        # -> convert result
        output_path = create_dir(os.path.join(config.DOWNLOAD_DIR, 'mag'))
        return citationfinder.store(filename=os.path.join(output_path, '{}.json'.format(author_id)))
    except(ObjectDoesNotExist) as e:
        raise e