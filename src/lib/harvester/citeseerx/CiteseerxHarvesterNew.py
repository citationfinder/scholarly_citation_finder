import string

from ..common.Harvester import Harvester
from sickle import Sickle

class CiteseerxHarvester(Harvester):
    
    OAI_PHM_URL = 'http://citeseerx.ist.psu.edu/oai2'
    
    FIELD_MAPPING = {
        'title': 'title',
        #'creator': 'authors',
        'description': 'abstract',
        'publisher': 'publisher',
        'rights': 'copyright'
        #subject
    }
    
    def __init__(self):
        super(CiteseerxHarvester, self).__init__('citeseerx')
    
    def harvest(self, _from='2015-12-05'):
        list_records_options = {}
        list_records_options['metadataPrefix'] = 'oai_dc'
        if _from:
            list_records_options['from'] = _from
        
        client = Sickle(self.OAI_PHM_URL)
        #harvestStart = datetime.strptime("2014-06-17T23:59:59Z", "%Y-%m-%dT%H:%M:%SZ")
        records = client.ListRecords(**{'metadataPrefix': 'oai_dc','from': '2015-12-05'})
        for record in records:
            metadata = record.metadata
            
            result_entry = {
                'urls': []
            }
    
            if 'creator' in metadata:
                result_entry['authors'] = metadata['creator']
            if 'date' in metadata:
                date = metadata['date'][-1]
                '''
                <dc:date>2009-04-19</dc:date>
                <dc:date>2007-11-19</dc:date>
                <dc:date>1998</dc:date>
                '''
                if len(date) == 4:
                    result_entry['date'] = date
            if 'source' in metadata:
                url = metadata['source'][0]
                if 'format' in metadata:
                    url = {
                        'value': url,
                        'type': metadata['format'][0]
                    }
                result_entry['urls'].append(url)
            for field in self.FIELD_MAPPING:
                if metadata[field]:
                    result_entry[self.FIELD_MAPPING[field]] = metadata[field][0]
            
            # <identifier>oai:CiteSeerX.psu:10.1.1.1.1519</identifier>
            result_entry['citeseerx_id'] = string.replace(record.header.identifier, 'oai:CiteSeerX.psu:', '')
            result_entry['urls'].append({
                'value': 'http://citeseerx.ist.psu.edu/viewdoc/download?doi={}&amp;rep=rep1&amp;type=pdf'.format(result_entry['citeseerx_id']),
                'type': 'application/pdf'
            })
            
            self.open_split_file()
            self.parse_publication2(result_entry)
            
            if self.check_stop_harvest():
                break

        self.stop_harvest()
