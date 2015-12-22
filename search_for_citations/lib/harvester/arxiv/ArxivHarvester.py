import string
from sickle import Sickle
from sickle.oaiexceptions import NoRecordsMatch

from ..common.Harvester import Harvester


class ArxivHarvester(Harvester):
    
    OAI_PHM_URL = 'http://export.arxiv.org/oai2'
    
    FIELD_MAPPING = {
        'title': 'title',
        #'creator': 'authors',
        'description': 'abstract',
        'publisher': 'publisher'
        #'subject': 'keywords'
    }
    
    def __init__(self, **kwargs):
        super(ArxivHarvester, self).__init__('arxiv', **kwargs)
    
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
        try:
            for record in client.ListRecords(**list_records_options):
                metadata = record.metadata
                result_entry = {
                    'urls': []
                }
                
                if 'creator' in metadata:
                    result_entry['authors'] = metadata['creator']
                if 'subject' in metadata:
                    result_entry['keywords'] = metadata['subject']
                if 'date' in metadata:
                    result_entry['date'] = metadata['date'][-1]
                if 'identifier' in metadata:
                    doi = metadata['identifier'][-1]
                    if 'doi:' in doi:
                        result_entry['doi'] = string.replace(doi, 'doi:', '')
                for field in self.FIELD_MAPPING:
                    if field in metadata:
                        result_entry[self.FIELD_MAPPING[field]] = metadata[field][0]
        
                # <identifier>oai:arXiv.org:10.1.1.1.1519</identifier>
                result_entry['arxiv_id'] = string.replace(record.header.identifier, 'oai:arXiv.org:', '')
                result_entry['urls'].append({
                    'value': 'http://arxiv.org/pdf/{}.pdf'.format(result_entry['arxiv_id']),
                    'type': 'application/pdf'
                })
                
                self.open_split_file()
                self.parse_publication2(result_entry)

                if self.check_stop_harvest():
                    break
        except(AttributeError, NoRecordsMatch) as e:
            self.logger.warn(str(e))
        finally:
            self.stop_harvest()
