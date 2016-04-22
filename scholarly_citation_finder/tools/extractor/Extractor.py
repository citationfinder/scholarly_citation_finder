
class ExtractorNotAvaiableException(Exception):
    pass


class Extractor(object):
    
    def extract_file(self, filename):
        raise Exception('Implement this method')