
class ExtractorNotAvaiableException(Exception):
    pass


class Extractor(object):
    '''
    Abstract extractor.
    '''
    
    def extract_file(self, filename):
        '''
        Extract a file
        
        :param filename: Name of the file
        '''
        raise Exception('Implement this method')