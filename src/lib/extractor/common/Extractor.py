import os.path

import codecs
from lxml import etree
from ...Parser import Parser
from ...utils import download_file
from config import DOWNLOAD_TMP_PATH
import requests

class Extractor(Parser):
    
    def __init__(self, name):
        super(Extractor, self).__init__(name+'_extractor')
    
    def extract_from_xml_file(self, filelist, func):
        if os.path.isfile(filelist):
            self.input = codecs.open(filelist, "r", "utf-8")
            self.output = codecs.open(filelist+'.tmp', "w", "utf-8")
            
            for line in self.input:
                self.output.write(line)
                if "<source>" in line:
                    line = line.replace('\t<source>', '')
                    url = line.replace('</source>\n', '')
                    #url = etree.fromstring(line).text
                    
                    print(url)
                    
                    response = requests.get(url)
                    #tmp_file = download_file(url, DOWNLOAD_TMP_PATH, self.count_citations)
                    if tmp_file:
                        self.count_citations += 1
                        self.output.write("\t<citations>\n")
                        func(tmp_file)
                        self.output.write("\t</citations>\n")
            return True
        else:
            raise IOError('File {} not found'.format(filelist))    