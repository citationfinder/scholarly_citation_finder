import os.path

import codecs
from lxml import etree

class Extractor:
    
    PREFIX = 'extractor_common'
    
    def extract(self, filename):
        if os.path.isfile(filename):
            self.f = codecs.open(filename, "r", "utf-8")
            self.output = codecs.open(filename+'.tmp', "w", "utf-8")            
            self._fast_iter()
            return True
        else:
            raise IOError('File {} not found'.format(filename))    
                
    def _fast_iter(self):
        
        for line in self.f:
            self.output.write(line)
            if "<source>" in line:
                #source = etree.fromstring(line).text
                self.output.write("\t<citations>\n")
                self.output.write("\t</citations>\n")
                