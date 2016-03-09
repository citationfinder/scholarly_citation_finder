from bs4 import BeautifulSoup
import requests
import re
from urlparse import urlparse
from requests.exceptions import ConnectionError
import logging

from scholarly_citation_finder.apps.core.models import PublicationUrl

logger = logging.getLogger(__name__)


class HtmlParserUnkownHeaderType(Exception):
    pass


class HtmlParser:
    '''
    Module to find a or multiple PDFs files on a HTML page.
    '''
    
    PDF_SEARCH_PATTERN = '(.*)pdf(.*)'

    def find_pdf_hyperrefs(self, url):
        '''
        Looks for hyperrefs to PDFs file on the provided website.
        
        :param url: HTML page
        :raise PdfFinderUnkownHeaderType:
        :raise ConnectionError:
        '''
        try:
            r = requests.get(url)
            r_type = r.headers.get('content-type')

            # the URL is already a PDF
            if PublicationUrl.MIME_TYPE_PDF in r_type:
                return r.url
            # the URL is a HTML page
            elif PublicationUrl.MIME_TYPE_HTML in r_type:
                return self.__find_hyperrefs(r.text, url=r.url, search_pattern=self.PDF_SEARCH_PATTERN)
            else:
                raise HtmlParserUnkownHeaderType('Unknown header type: {}'.format(r_type))
        except(ConnectionError) as e:
            raise e

    def __find_hyperrefs(self, html, url, search_pattern='(.*)'):
        '''
        Looks for hyperrefs to PDFs file in the provided HTML string.
        
        :param html: HTML string
        :param url: URL the HTML was downloaded from. It is used to convert relative URLs to absolute ones
        :param search_pattern: Search pattern for re.compile
        :return 
        '''
        results = []
        parsed_uri = urlparse(url)
        url_domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

        soup = BeautifulSoup(html, 'lxml')
        # Get all links, which contains the string 'pdf'
        for link in soup.findAll('a', attrs={'href': re.compile(search_pattern)}):
            href = link.get('href')
            # Convert relativ urls to absolute url
            if href.startswith(('http://', 'https://', 'ftp://')):
                pass
            elif href.startswith('/'):
                href = url_domain + href
            else:
                href = url + href

            if href not in results:
                results.append(href)
        return results
