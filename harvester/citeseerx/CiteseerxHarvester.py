from django.http import HttpResponse
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from search_for_citations.models import Publication

class CiteseerxHarvester:
    
    OAI_PHM_URL = 'http://citeseerx.ist.psu.edu/oai2'
    
    def harvest(self):
        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        client = Client(self.OAI_PHM_URL, registry)
        #harvestStart = datetime.strptime("2014-06-17T23:59:59Z", "%Y-%m-%dT%H:%M:%SZ")
        for record in client.listRecords(metadataPrefix='oai_dc'):
            header = record[0];
            metadata = record[1];
    
            title = ''
            abstract = ''
            source = ''
    
            if metadata['title']:
                title = metadata['title'][0]
            if metadata['description']:
                abstract = metadata['description'][0]
            if metadata['source']:
                source = metadata['source'][0]
                  
            publication = Publication(
                title=title,
                abstract=abstract,
                source=source,
                citeseerx_id=header.identifier())
            publication.save()
            
            for author in metadata['creator']:
                #a = Author(last_name=unidecode(author))
                #publication.authors.add(a)
                publication.authors.create(last_name=author)
            print('save')      