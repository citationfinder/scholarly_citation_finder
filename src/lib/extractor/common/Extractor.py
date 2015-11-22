import os.path

import codecs
from lxml import etree
from ...harvester.common.Harvester import Harvester
from ...utils import download_file
from config import DOWNLOAD_TMP_PATH

class Extractor(Harvester):
    
    PREFIX = 'extractor_common'
    
    def extract_from_xml_file(self, filename, func):
        if os.path.isfile(filename):
            self.input = codecs.open(filename, "r", "utf-8")
            self.output = codecs.open(filename+'.tmp', "w", "utf-8")
            
            for line in self.input:
                self.output.write(line)
                if "<source>" in line:
                    url = etree.fromstring(line).text
                    filename = download_file(url, DOWNLOAD_TMP_PATH)
                    if filename:
                        func(filename)
                    #source = etree.fromstring(line).text
                    self.output.write("\t<citations>\n")
                    self.output.write("\t</citations>\n")
                            
            
                     
            self._fast_iter()
            return True
        else:
            raise IOError('File {} not found'.format(filename))    