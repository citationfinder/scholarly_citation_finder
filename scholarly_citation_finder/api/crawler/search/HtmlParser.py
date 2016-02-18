from bs4 import BeautifulSoup
import requests
import re
from urlparse import urlparse
from requests.exceptions import ConnectionError
import logging

logger = logging.getLogger(__name__)

class HtmlParserUnkownHeaderType(Exception):
    pass

class HtmlParser:
    '''
    Module to find a or multiple PDFs files on a HTML page.
    '''

    MIMETYPE_PDF = 'application/pdf'
    MIMETYPE_HTML = 'text/html'

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
            if self.MIMETYPE_PDF in r_type:
                return url
            # the URL is a HTML page
            elif self.MIMETYPE_HTML in r_type:
                return self.__find_hyperrefs(r.text, url=url, search_pattern='(.*)pdf(.*)')
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
        result = []
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
            result.append(href)
        return result