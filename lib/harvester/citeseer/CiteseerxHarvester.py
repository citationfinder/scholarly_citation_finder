import string
import logging

from ..common.Harvester import Harvester
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader


class CiteseerxHarvester(Harvester):
    
    OAI_PHM_URL = 'http://citeseerx.ist.psu.edu/oai2'
    
    PREFIX = 'citeseerx_'
    
    def harvest(self):
        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        client = Client(self.OAI_PHM_URL, registry)
        #harvestStart = datetime.strptime("2014-06-17T23:59:59Z", "%Y-%m-%dT%H:%M:%SZ")
        for record in client.listRecords(metadataPrefix='oai_dc'):
            header = record[0];
            metadata = record[1];
    
            title = ''
            date = ''
            publisher = ''
            abstract = ''
            source = ''
    
            if metadata['title']:
                title = metadata['title'][0]
            if metadata['date']:
                date = metadata['date'][-1]
                '''
                <dc:date>2009-04-19</dc:date>
                <dc:date>2007-11-19</dc:date>
                <dc:date>1998</dc:date>
                '''
                if len(date) != 4:
                    date = ''
            if metadata['description']:
                abstract = metadata['description'][0]
            if metadata['publisher']:
                publisher = metadata['publisher'][0]
            #if metadata['source']:
            #    source = metadata['source'][0]
            
            # <identifier>oai:CiteSeerX.psu:10.1.1.1.1519</identifier>
            citeseerx_id = string.replace(header.identifier(), 'oai:CiteSeerX.psu:', '')
            source = "http://citeseerx.ist.psu.edu/viewdoc/download?doi="+citeseerx_id+"&rep=rep1&type=pdf"            
            
            self.parse_publication(
                authors=metadata['creator'],
                title=title,
                date=date,
                publisher=publisher,
                abstract=abstract,
                source=source,
                citeseerx_id=citeseerx_id)
            
        
        self.stop_harvest()
        
if __name__ == '__main__':
    harvester = CiteseerxHarvester()
    harvester.harvest()