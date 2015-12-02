import codecs
import os.path

import config
from lib.utils import download_file
from ...Parser import Parser

class Extractor(Parser):
    
    def __init__(self, name):
        super(Extractor, self).__init__('{}_extractor'.format(name))
    
    def extract_from_xml_file(self, file_publications, func):
        if os.path.isfile(file_publications):
            self.input = codecs.open(file_publications, "r", "utf-8")
            self.output.open('{}.tmp.xml'.format(file_publications[:-4])) # ending .xml is 4 characters long

            for line in self.input:
                self.output.write(line)
                if "<source>" in line:
                    line = line.replace('\t\t<source>', '')
                    url = line.replace('</source>\n', '')
                    #url = etree.fromstring(line).text
                    
                    tmp_file = download_file(url, config.DOWNLOAD_TMP_DIR, '{}.pdf'.format(self.count_citations))
                    if tmp_file:
                        self.count_citations += 1
                        func(tmp_file)

            self.output.close()
            return True
        else:
            raise IOError('File {} not found'.format(file_publications))    