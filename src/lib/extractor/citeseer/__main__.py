from ..common.Extractor import get_arguments
from .CiteseerExtractor import CiteseerExtractor

if __name__ == '__main__':
    file_publications, limit = get_arguments()
    
    extractor = CiteseerExtractor(limit=limit)
    if file_publications:
        extractor.extract_from_xml_file(file_publications)