from __future__ import absolute_import
from celery import shared_task
import os.path
import logging
import requests
from django.core.exceptions import ObjectDoesNotExist

from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import create_dir
from scholarly_citation_finder.apps.citation.CitationFinder import CitationFinder


logger = logging.getLogger(__name__)


@shared_task
def citations(author_name, author_id, publin_callback_url=None):
    try:
        citationfinder = CitationFinder(database='mag')
        author_id, length_publication_set = citationfinder.publication_set.set_by_author(name=author_name, id=author_id)
        logger.info('set {} publications by author {}'.format(length_publication_set, author_id))
        citationfinder.hack()
        citationfinder.citations = citationfinder.citing_papers
    
        # -> convert result
        output_filename = citationfinder.store(path=create_dir(os.path.join(config.DOWNLOAD_TMP_DIR, 'mag')),
                                               filename=author_id)
        if publin_callback_url:
            __publin_callback(publin_callback_url, output_filename)
        else:
            return output_filename
    except(ObjectDoesNotExist) as e:
        raise e
    except(Exception) as e:
        raise e


def __publin_callback(callback_url, output_filename):
    with open(output_filename, 'r') as output_file:
        r = requests.post(callback_url,
                          params={'p': 'submit', 'm': 'bulkimportapi'},
                          data={'input': output_file.read()})
    if r.status_code == 202:
        return r.text
    else:
        raise Exception('Expected 202 as response, but get {}'.format(r.status_code))
