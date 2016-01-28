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
        super(CiteseerxHarvester, self).__init__('dblp', **kwargs)
    
    def harvest(self, limit=None, _from=None, until=None):
        self.limit = limit

        list_records_options = {
            'metadataPrefix': 'oai_dc'
        }
        if _from:
            list_records_options['from'] = _from
        if until:
            list_records_options['until'] = until
        
        client = Sickle(self.OAI_PHM_URL)
        records = client.ListRecords(**list_records_options)
        try:
            for record in records:
                metadata = record.metadata
                result_entry = {
                    'urls': []
                }
            
                if 'creator' in metadata:
                    result_entry['authors'] = metadata['creator']
                if 'subject' in metadata:
                    result_entry['keywords'] = metadata['subject']
                if 'date' in metadata:
                    date = metadata['date'][-1]
                    '''
                    <dc:date>2009-04-19</dc:date>
                    <dc:date>2007-11-19</dc:date>
                    <dc:date>1998</dc:date>
                    '''
                    if len(date) == 4:
                        result_entry['year'] = date
                if 'source' in metadata:
                    url = metadata['source'][0]
                    if 'format' in metadata:
                        url = {
                            'value': url,
                            'type': metadata['format'][0]
                        }
                    result_entry['urls'].append(url)
                for field in self.FIELD_MAPPING:
                    if field in metadata:
                        result_entry[self.FIELD_MAPPING[field]] = metadata[field][0]
                    
                # <identifier>oai:CiteSeerX.psu:10.1.1.1.1519</identifier>
                result_entry['citeseerx_id'] = string.replace(record.header.identifier, 'oai:CiteSeerX.psu:', '')
                result_entry['urls'].append({
                    'value': 'http://citeseerx.ist.psu.edu/viewdoc/download?doi={}&amp;rep=rep1&amp;type=pdf'.format(result_entry['citeseerx_id']),
                    'type': 'application/pdf'
                })

                self.parse_publication(result_entry)
                    
                if self.check_stop_harvest():
                    break
        except(AttributeError, NoRecordsMatch) as e:
            self.logger.warn(str(e))
        finally:
            self.stop_harvest()
