from __future__ import absolute_import
from celery import shared_task
import os.path
import logging
import requests
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import create_dir
from scholarly_citation_finder.apps.citation.CitationFinder import CitationFinder,\
    EmptyPublicationSetException, NoCitationsFoundExeception


logger = logging.getLogger(__name__)


@shared_task
def citations(type, name=None, id=None, publin_callback_url=None, isi_fieldofstudy=False, database='mag'):
    '''
    Task to find citations in the MAG.
    
    :param type: 'author', 'conference' or 'journal'
    :param name: Name of the entry
    :param id: ID of the entry
    :param publin_callback_url: Callback URL
    :param isi_fieldofstudy: If true, convernt field of studies to ISI field
    :param database: Database name
    :return: Name of the output file
    :raise ObjectDoesNotExits:
    :raise MultipleObjectsReturned:
    :raise EmptyPublicationSetException:
    :raise Exception: When type is unknown
    '''
    try:
        citationfinder = CitationFinder(database=database)
        if type == 'author':
            id, length_publication_set = citationfinder.publication_set.set_by_author(name=name, id=id)
        elif type == 'conference':
            id, length_publication_set = citationfinder.publication_set.set_by_conference(name=name, id=id)            
        elif type == 'journal':
            id, length_publication_set = citationfinder.publication_set.set_by_journal(name=name, id=id)
        else:
            raise Exception('Unknown type: {}'.format(type))
        logger.info('set {} publications by {} {}'.format(length_publication_set, type, id))
        
        citationfinder.load_stored_citations()
        citationfinder.citations = citationfinder.stored_citations
    
        # -> convert result
        output_filename = citationfinder.store(path=create_dir(os.path.join(config.DOWNLOAD_TMP_DIR, 'mag')),
                                               filename=id,
                                               isi_fieldofstudy=isi_fieldofstudy)
        if publin_callback_url:
            __publin_callback(publin_callback_url, output_filename)
        else:
            return output_filename
    except(ObjectDoesNotExist, MultipleObjectsReturned, EmptyPublicationSetException, NoCitationsFoundExeception) as e:
        raise e
    #except(Exception) as e:
    #    raise e


def __publin_callback(callback_url, output_filename):
    '''
    Send data to callback URL.
    
    :param callback_url: Callback URL
    :param output_filename: Stored output file
    '''
    with open(output_filename, 'r') as output_file:
        r = requests.post(callback_url,
                          params={'p': 'submit', 'm': 'bulkimportapi'},
                          data={'input': output_file.read()})
    if r.status_code == 202:
        return r.text
    else:
        raise Exception('Expected 202 as response, but get {}'.format(r.status_code))
