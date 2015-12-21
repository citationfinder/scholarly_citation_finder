import codecs
import getopt
import os.path
import sys
from lxml import etree

from search_for_citations import config
from ...utils import download_file_pdf
from ...Parser import Parser


def get_arguments():
    argv = sys.argv[1:]
    try:
        opts, _ = getopt.getopt(argv, 'hf:l:', ['help', 'file=', 'limit='])
    except getopt.GetoptError as e:
        print(str(e))
        print('Usage: -h for help')
        sys.exit(2)
    
    limit = None
    file_publications = None
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: my-process.py -s <start> -e <end>')
            sys.exit()
        elif opt in ('-f', '--file'):
            file_publications = arg.strip()
        elif opt in ('-l', '--limit'):
            limit = int(arg)
        else:
            raise Exception('unhandled option')
    return (file_publications, limit)


class Extractor(Parser):
    
    def __init__(self, name, limit=None):
        super(Extractor, self).__init__('{}_extractor'.format(name))
        self.count_extracted_papers = 0
        self.limit = limit
    
    def extract_from_xml_file(self, file_publications, func):
        if os.path.isfile(file_publications):
            self.logger.info('start to extract from {}'.format(file_publications))
            self.input = codecs.open(file_publications, "r", "utf-8")
            self.output.open('{}.tmp.xml'.format(file_publications[:-4]))  # ending .xml is 4 characters long

            for line in self.input:
                self.output.write(line)
                # TODO: Handle multiple URLs
                if '<url type="application/pdf">http://citeseerx.ist.psu.edu/' in line:
                    #line = line.replace('\t\t<source>', '')
                    #url = line.replace('</source>\n', '')
                    #url = url.replace('&amp;', '&')  # otherwise download from citeseer does not work
                    url = etree.fromstring(line).text
                    self.logger.debug('url: {}'.format(url))

                    tmp_file = download_file_pdf(url, path=config.DOWNLOAD_TMP_DIR, name='{}.pdf'.format(self.count_extracted_papers))
                    #tmp_file = os.path.join(config.DOWNLOAD_TMP_DIR, '{}.pdf'.format(self.count_extracted_papers))
                    if tmp_file and not self.check_stop_extract():
                        self.count_extracted_papers += 1
                        func(tmp_file)
                        
                    #if self.check_stop_extract():
                    #    break

            self.stop_extract()
            return True
        else:
            raise IOError('File {} not found'.format(file_publications))
        
    def stop_extract(self):
        self.logger.info('Stop extraction')
        self.output.close()
        
    def check_stop_extract(self):
        return self.limit and self.count_extracted_papers >= self.limit