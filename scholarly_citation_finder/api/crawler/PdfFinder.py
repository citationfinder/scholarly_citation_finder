from bs4 import BeautifulSoup
import requests
import re
from urlparse import urlparse
from requests.exceptions import ConnectionError
import logging

logger = logging.getLogger(__name__)


class PdfFinder:
    '''
    Module to find a or multiple PDFs files on a HTML page.
    '''

    MIMETYPE_PDF = 'application/pdf'
    MIMETYPE_HTML = 'text/html'

    def find_pdf(self, url):
        '''
        Looks for PDFs files on the provided website.
        
        :param url: HTML page
        '''
        hyperrefs = self.find_hyperrefs(url)
        if hyperrefs:
            for link in hyperrefs:
                if link.endswith('.pdf') or link.endswith('/pdf'):
                    return link
            return hyperrefs[-1]
        return False

    def find_hyperrefs(self, url):
        '''
        Looks for hyperrefs to PDFs file on the provided website.
        
        :param url: HTML page
        '''
        try:
            r = requests.get(url)
            r_type = r.headers.get('content-type')

            # the URL is already a PDF
            if r_type in self.MIMETYPE_PDF:
                return url
            # the URL is a HTML page
            elif r_type in self.MIMETYPE_HTML:
                return self.find_hyperrefs_from_html(r.text, url)
            else:
                logger.debug('Unknown header type: {}'.format(r_type))
        except(ConnectionError) as e:
            logger.info(e, exc_info=True)

        return False

    def find_hyperrefs_from_html(self, html, url):
        '''
        Looks for hyperrefs to PDFs file in the provided HTML string.
        
        :param html: HTML string
        :param url: URL the HTML was downloaded from. It is used to convert relative URLs to absolute ones
        '''
        result = []
        parsed_uri = urlparse(url)
        url_domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

        soup = BeautifulSoup(html, 'lxml')
        # Get all links, which contains the string 'pdf'
        for link in soup.findAll('a', attrs={'href': re.compile('(.*)pdf(.*)')}):
            href = link.get('href')
            # Convert relativ urls to absolute url
            if href.startswith(('http://', 'https://')):
                pass
            elif href.startswith('/'):
                href = url_domain + href
            else:
                href = url + href
            result.append(href)
        return result
