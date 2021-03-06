import logging
import re
from sickle import Sickle
from sickle.oaiexceptions import NoRecordsMatch
from requests.exceptions import ChunkedEncodingError, ConnectionError

from scholarly_citation_finder.tools.harvester.Harvester import Harvester
from scholarly_citation_finder.apps.parser.Exceptions import ParserConnectionError,\
    ParserRollbackError

logger = logging.getLogger(__name__)


class OaiHarvester(Harvester):
    '''
    OAI harvester to collect meta data from OAI provider.
    '''
    
    FIELD_MAPPING = {
        'title': 'title',
        'description': 'abstract',
        'publisher': 'publisher',
        'rights': 'copyright' # <- citeseerx only
    }    
    
    oai_url = None
    
    def __init__(self, name, oai_url, **kwargs):
        '''
        Create object.
        
        :param name: Harvester name
        :param oai_url: OAI URL
        '''
        super(OaiHarvester, self).__init__(name=name, **kwargs)
        self.oai_url = oai_url
    
    def harvest(self, limit=None, _from=None, until=None, _from_id=None, resumptionToken=None):
        '''
        Harvest OAI data provider.
        
        :param limit: Number of maximum publications to parse
        :param _from: OAI-PHM from date YYYY-MM-DD
        :param until: OAI-PHM until date YYYY-MM-DD
        :param _from_id: Last stored (!) identifier, e.g. '10.1.1.1.1519'
        :param resumptionToken: OAI-PHM resumption token, e.g. '10.1.1.102.634-467085-20500-oai_dc'
        :return: Number of parsed publications or False    
        '''
        self.set_limit(limit)

        list_records_options = {}
        if resumptionToken is not None:
            list_records_options['resumptionToken'] = resumptionToken
        else:
            list_records_options['metadataPrefix'] = 'oai_dc'
            if _from:
                list_records_options['from'] = _from
            if until:
                list_records_options['until'] = until
        
        # TODO: move to parent class
        try:    
            self.start_harevest(logger_string='limit={}, from={}, until={}, from_id={}, resumptionToken={}'.format(limit, _from, until, _from_id, resumptionToken))
            num_publications = self.harvest_oai_phm(list_records_options, _from_id=_from_id)
            self.stop_harvest()
            return num_publications
        except(ParserConnectionError) as e:
            logger.warn(str(e))
            self.stop_harvest() # commit results
            # TODO: restart, if it was not a: requests.exceptions.ConnectionError: ('Connection aborted.', error(104, 'Connection reset by peer'))

            search_resumptionToken = re.search(r'resumptionToken=[^ ]+', str(e)) # [...]ds&resumptionToken=10.1.1.104.424-327119-34500-oai_dc (Ca[...]
            if search_resumptionToken:
                search_resumptionToken = search_resumptionToken.group(0).replace('resumptionToken=', '')
                return self.harvest(resumptionToken=search_resumptionToken)
            else:
                return False
        except(ParserRollbackError) as e:
            # TODO: rollback already happend, restart from last point
            return False
        
    def harvest_oai_phm(self, list_records_options, _from_id=None):
        '''
        Harvest OAI-PHM.
        
        :param list_records_options: List records option for Sickle
        :param _from_id: Last stored (!) identifier, e.g. '10.1.1.1.1519'
        :return: Number of parsed publications or False
        :raise ParserRollbackError: see Parser.parse
        '''

        try:
            client = Sickle(self.oai_url)
            records = client.ListRecords(**list_records_options)

            for record in records:
                identifier = record.header.identifier.split(':')[2] # '<identifier>scheme:namespace-identifier:local-identifier</identifier>
                # last_datestamp = record.header.datestamp
                if _from_id is not None:
                    if _from_id == identifier:
                        _from_id = None
                    continue
                
                metadata = record.metadata
                
                publication = {}
                authors = []
                keywords = []
                urls = []
            
                if 'creator' in metadata:
                    authors = metadata['creator']
                if 'subject' in metadata:
                    keywords = metadata['subject']
                if 'date' in metadata:
                    if self.name == 'citeseerx':
                        date = metadata['date'][-1]
                        '''
                        <dc:date>2009-04-19</dc:date>
                        <dc:date>2007-11-19</dc:date>
                        <dc:date>1998</dc:date>
                        '''
                        if len(date) == 4:
                            publication['year'] = date
                        del date
                    elif self.name == 'arxiv':
                        publication['year'] = metadata['date'][0][:4]
                # citeseerx only
                if 'source' in metadata:
                    url = metadata['source'][0]
                    if 'format' in metadata:
                        url = {
                            'value': url,
                            'type': metadata['format'][0]
                        }
                    urls.append(url)
                    del url
                # arxiv only
                if 'identifier' in metadata:
                    doi = metadata['identifier'][-1]
                    if 'doi:' in doi:
                        publication['doi'] = doi.replace('doi:', '')
                    del doi
                for field in self.FIELD_MAPPING:
                    if field in metadata:
                        publication[self.FIELD_MAPPING[field]] = metadata[field][0]

                publication['source'] = self.name+':'+identifier

                self.parser.parse(publication,
                                  authors=authors,
                                  keywords=keywords,
                                  urls=urls)
                    
                if self.check_stop_harvest():
                    break
                
            return self.parser.count_publications
        # sickle errors => oai-phm errors
        except(NoRecordsMatch) as e:
            return False
        # requests (part of sickle) errors => connection errors
        except(ConnectionError, ChunkedEncodingError) as e: # incorrect chunked encoding
            raise ParserConnectionError(str(e))
        # database errors
        except(ParserRollbackError) as e:
            raise e
