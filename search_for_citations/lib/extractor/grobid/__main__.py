from ..Extractor import get_arguments
from .GrobidExtractor import GrobidExtractor

if __name__ == '__main__':
    file_publications, limit = get_arguments()
    
    extractor = GrobidExtractor(limit=limit)
    if file_publications:
    	#extractor.logger.debug('extract {}'.format(file_publications))
        extractor.extract_from_xml_file(file_publications)
    extractor.logger.debug('nothing to do')
