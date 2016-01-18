import os.path

from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import create_dir, download_file, extract_file
from scholarly_citation_finder.lib.process import ProcessException, external_process

MAG_DOWNLOAD_URL = 'https://academicgraph.blob.core.windows.net/graph-2015-11-06/MicrosoftAcademicGraph.zip'

def download_and_extract_data(download_dir):
    try:
        file = download_file(MAG_DOWNLOAD_URL, download_dir)
        return extract_file(file, download_dir)
    except(ProcessException) as e:
        #logger.warn('{}: {}'.format(type(e).__name__), str(e))
        return False

def normalize_files(type, download_dir):    
    exit_status, stdout, stderr = external_process(['python', 'normalize_files.py', os.path.join(download_dir, 'Authors.txt')],
                                                   cwd=os.path.join('scholarly_citation_finder', 'apps', 'harvester', 'mag'))
    print(exit_status)
    print(stdout)
    print(stderr)    
    
if __name__ == '__main__':
    normalize_files(None, config.DOWNLOAD_DIR)


            
        # prepare

