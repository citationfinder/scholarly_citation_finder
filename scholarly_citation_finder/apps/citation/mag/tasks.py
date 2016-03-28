from __future__ import absolute_import
from celery import shared_task
import os.path
import logging
import requests
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import create_dir
from scholarly_citation_finder.apps.citation.CitationFinder import CitationFinder,\
    EmptyPublicationSetException


logger = logging.getLogger(__name__)


@shared_task
def citations(type, name=None, id=None, publin_callback_url=None, isi_fieldofstudy=False, database='mag'):
    '''
    
    :param type:
    :param name:
    :param id:
    :param publin_callback_url:
    :return: 
    :raise ObjectDoesNotExits:
    :raise MultipleObjectsReturned:
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
        logger.info('set {} publications by {} {}'.format(length_publication_set, type, id))
        
        citationfinder.hack()
        citationfinder.citations = citationfinder.citing_papers
    
        # -> convert result
        output_filename = citationfinder.store(path=create_dir(os.path.join(config.DOWNLOAD_TMP_DIR, 'mag')),
                                               filename=id,
                                               isi_fieldofstudy=isi_fieldofstudy)
        if publin_callback_url:
            __publin_callback(publin_callback_url, output_filename)
        else:
            return output_filename
    except(ObjectDoesNotExist, MultipleObjectsReturned, EmptyPublicationSetException) as e:
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
