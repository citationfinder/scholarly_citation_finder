from bs4 import BeautifulSoup
import requests
import re
from urlparse import urlparse
from requests.exceptions import ConnectionError
import logging
logger = logging.getLogger(__name__)


class SearchPdf:

    MIMETYPE_PDF = 'application/pdf'
    MIMETYPE_HTML = 'text/html'

    def get_pdf(self, url):
        links = self.get_links(url)
        if links:
            for link in self.get_links(url):
                if link.endswith('.pdf') or link.endswith('/pdf'):
                    return link
            return links[-1]
        return False

    def get_links_from_html(self, html, url):
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

    def get_links(self, url):
        try:
            r = requests.get(url)
            r_type = r.headers.get('content-type')

            if r_type in self.MIMETYPE_PDF:
                return url
            elif r_type in self.MIMETYPE_HTML:
                return self.get_links_from_html(r.text, url)
            else:
                logger.debug('Unknown header type: {}'.format(r_type))
        except(ConnectionError) as e:
            logger.debug(str(e))

        return False
