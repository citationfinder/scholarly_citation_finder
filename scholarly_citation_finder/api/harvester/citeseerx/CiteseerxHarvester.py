import string
from sickle import Sickle
from sickle.oaiexceptions import NoRecordsMatch

from ..Harvester import Harvester


class CiteseerxHarvester(Harvester):
    
    OAI_PHM_URL = 'http://citeseerx.ist.psu.edu/oai2'
    
    FIELD_MAPPING = {
        'title': 'title',
        #'creator': 'authors',
        'description': 'abstract',
        'publisher': 'publisher',
        'rights': 'copyright'
        #'subject': 'keywords'
    }
    
    def __init__(self, **kwargs):
        super(CiteseerxHarvester, self).__init__('citeseerx', **kwargs)
    
    def harvest(self, limit=None, _from=None, until=None):
        '''
        
        :param limit: Number of maximum publications to parse
        :param _from: OAI-PHM from date YYYY-MM-DD
        :param until: OAI-PHM until date YYYY-MM-DD
        :return: Number of parsed publications        
        '''
        
        self.limit = limit

        list_records_options = {
            'metadataPrefix': 'oai_dc'
        }
        if _from:
            list_records_options['from'] = _from
        if until:
            list_records_options['until'] = until
            
        self.start_harevest()
        num_publications = self.harvest_oai_phm(list_records_options)
        self.stop_harvest()
        return num_publications
        
    def harvest_oai_phm(self, list_records_options):
        '''
        
        :param list_records_options: List records option for Sickle
        :return: Number of parsed publications or False
        :raise ParserRollbackError: see Parser.parse
        '''
        
        
        client = Sickle(self.OAI_PHM_URL)
        records = client.ListRecords(**list_records_options)
        try:
            for record in records:
                metadata = record.metadata
                
                publication = {}
                journal = None
                authors = []
                keywords = []
                urls = []
            
                if 'creator' in metadata:
                    authors = metadata['creator']
                if 'subject' in metadata:
                    keywords = metadata['subject']
                if 'date' in metadata:
                    date = metadata['date'][-1]
                    '''
                    <dc:date>2009-04-19</dc:date>
                    <dc:date>2007-11-19</dc:date>
                    <dc:date>1998</dc:date>
                    '''
                    if len(date) == 4:
                        publication['year'] = date
                if 'source' in metadata:
                    url = metadata['source'][0]
                    if 'format' in metadata:
                        url = {
                            'value': url,
                            'type': metadata['format'][0]
                        }
                    urls.append(url)
                for field in self.FIELD_MAPPING:
                    if field in metadata:
                        publication[self.FIELD_MAPPING[field]] = metadata[field][0]
                    
                # <identifier>oai:CiteSeerX.psu:10.1.1.1.1519</identifier>
                publication['source'] = 'citeseerx:'+string.replace(record.header.identifier, 'oai:CiteSeerX.psu:', '')
                #urls.append({
                #    'value': 'http://citeseerx.ist.psu.edu/viewdoc/download?doi={}&amp;rep=rep1&amp;type=pdf'.format(result_entry['citeseerx_id']),
                #    'type': 'application/pdf'
                #})

                self.parse(publication, journal, authors, keywords, urls)
                    
                if self.check_stop_harvest():
                    break
                
            return self.count_publications
        except(AttributeError, NoRecordsMatch) as e:
            self.logger.error(e, exc_info=True)
            return False
