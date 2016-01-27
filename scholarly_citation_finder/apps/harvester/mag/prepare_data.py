from scholarly_citation_finder.lib.file import download_file_process, extract_file_process
from scholarly_citation_finder.lib.process import ProcessException

MAG_DOWNLOAD_URL = 'https://academicgraph.blob.core.windows.net/graph-2015-11-06/MicrosoftAcademicGraph.zip'

def download_and_extract_data(download_dir):
    try:
        file = download_file_process(MAG_DOWNLOAD_URL, download_dir)
        return extract_file_process(file, download_dir)
    except(ProcessException) as e:
        #logger.warn('{}: {}'.format(type(e).__name__), str(e))
        return False

def normalize_files(type, download_dir):    
    pass
