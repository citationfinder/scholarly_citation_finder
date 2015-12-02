import codecs
import getopt
import os.path
import sys

import config
from lib.utils import download_file
from ...Parser import Parser

class Extractor(Parser):
    
    def __init__(self, name):
        super(Extractor, self).__init__('{}_extractor'.format(name))
        self.count_extracted_papers = 0
        self.file_publications, self.limit = self.get_arguments(sys.argv[1:])
    
    def get_arguments(self, argv):
        try:
            opts, _ = getopt.getopt(argv, "hf:l:", ["help", "file=", "limit="])
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
            elif opt in ("-f", "--file"):
                file_publications = arg.strip();
            elif opt in ("-l", "--limit"):
                limit = int(arg);
            else:
                raise Exception("unhandled option")
        return (file_publications, limit)
    
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
                    
                    tmp_file = download_file(url, config.DOWNLOAD_TMP_DIR, '{}.pdf'.format(self.count_extracted_papers))
                    #tmp_file = os.path.join(config.DOWNLOAD_TMP_DIR, '{}.pdf'.format(self.count_citations))
                    if tmp_file:
                        self.count_extracted_papers += 1
                        func(tmp_file)
                        
                    if self.check_stop_harvester():
                        break

            self.stop_extract()
            return True
        else:
            raise IOError('File {} not found'.format(file_publications))
        
    def stop_extract(self):
        self.output.close()  
        
    def check_stop_harvester(self):
        return self.limit and self.count_extracted_papers >= self.limit
