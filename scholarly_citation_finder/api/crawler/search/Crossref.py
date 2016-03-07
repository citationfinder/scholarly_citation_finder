import requests
import logging
from requests.exceptions import ConnectionError

logger = logging.getLogger(__name__)


class CrossrefUnwantedType(Exception):
    pass


class CrossrefResponseException(Exception):
    pass


class Crossref:   
    '''
    
    @see: http://api.crossref.org/
    '''

    
    API_URL = 'http://api.crossref.org/'

    MAPPING = {'type': 'type',
               'publisher': 'publisher',
               'issue': 'issue',
               'DOI': 'doi',
               'volumne': 'volumne',
               'subject': 'keywords'}
    
    API_ENDPOINT_WORKS = 'works'
    API_RESPONSE_STATUS = 'status'
    API_RESPONSE_STATUS_OK = 'ok'
    API_RESPONSE_ESSAGE = 'message'
    API_RESPONSE_MESSAGE_TYPE = 'message-type'
    
    def query(self, resource, query=None, filter=None, sort=None, order=None):
        try:
            params = {'query': query,
                      'filter': filter,
                      'sort': sort,
                      'order': order}
            url = self.API_URL + resource
            r = requests.get(url, params=params)

            if r.status_code != 200:
                raise CrossrefResponseException('Expected response status code 200, but it is  {}'.format(r.status_code))
                  
            j = r.json()
            if j[self.API_RESPONSE_STATUS] != self.API_RESPONSE_STATUS_OK:
                raise CrossrefResponseException('Expected response status "ok", but it is "{}": '.format(j[self.API_RESPONSE_STATUS], j[self.API_RESPONSE_ESSAGE]))
            return j[self.API_RESPONSE_MESSAGE_TYPE], j[self.API_RESPONSE_ESSAGE]
        except(ConnectionError) as e:
            raise e
        
    def query_works(self, **kwargs):
        _, message = self.query(self.API_ENDPOINT_WORKS, **kwargs)
        results = []
        for item in message['items']:
            try:
                results.append(self.__parse_publication(item))
            except(CrossrefUnwantedType) as e:
                logger.info(str(e))
        return results

    def query_works_doi(self, doi, **kwargs):
        _, message = self.query('{}/{}'.format(self.API_ENDPOINT_WORKS, doi))
        return self.__parse_publication(message)
    
    def __parse_publication(self, item):
        if 'type' not in item:
            raise CrossrefUnwantedType('Unwanted Crossref type: no type') 

        result = {}
        container_title = None
        
        for key, value in item.iteritems():
            if key == 'type':
                if value in ('proceedings-article', 'paper-conference'):
                    result[key] = 'inproceedings'
                elif 'article' in value:  # "article", "article-journal"
                    result[key] = 'article'
                elif value in ('chapter', 'book-chapter', 'inbook'):
                    result[key] = 'incollection'
                elif value == 'book':
                    result[key] = value
                elif value == 'thesis':
                    result[key] = 'phdthesis'
                else: # reference-entry, journal, dataset, component, standard
                    raise CrossrefUnwantedType('Unwanted Crossref type: {}'.format(value)) 
            elif key == 'title' and len(value) > 0:
                result['title'] = value[0]
            elif key == 'container-title' and len(value) > 0:
                container_title = value[-1].title()
            elif key == 'page':
                tmp = value.split('-')
                result['page_from'] = tmp[0]
                if len(tmp) == 2:
                    result['page_to'] = tmp[1]
                del tmp
            elif key == 'published-online' and 'date-parts' in value:
                result['year'] = value['date-parts'][0][0]
            elif key == 'license' and 'URL' in value:
                result['copyright'] = value['URL']
            elif key in self.MAPPING:
                result[self.MAPPING[key]] = value
            # relation: author
            elif key == 'author':
                result['authors'] = []
                for author in value:
                    name = author['family']
                    if 'given' in author:
                        name += ', ' + author['given']
                    result['authors'].append(name)
            # relation urls
            elif key == 'link':
                result['urls'] = []
                for url in value:
                    result['urls'].append('{},{}'.format(url['content-type'], url['URL']))
        
        if container_title:
            if result['type'] == 'inproceedings':
                result['conference_name'] = container_title
            elif result['type'] == 'article':
                result['journal_name'] = container_title           
            elif result['type'] in ('incollection', 'book'):
                result['booktitle'] = container_title
            else:
                result['container-title'] = container_title           
            
        return result
