import os.path
from settings.development import BASE_DIR


def get_abspath(path):
    return os.path.abspath(os.path.join(BASE_DIR, path))

TEST_DIR = get_abspath('../test')
DOWNLOAD_DIR = get_abspath('../downloads')
DOWNLOAD_TMP_DIR = os.path.join(DOWNLOAD_DIR, 'tmp')
LOG_DIR = get_abspath('../log')

# Harvester
HARVESTER_DBLP_DIR = BASE_DIR
HARVESTER_CITESEERX_DIR = BASE_DIR
HARVESTER_ARXIV_DIR = BASE_DIR
# Extractor
EXTRACTOR_CITESEER_DIR = BASE_DIR
EXTRACTOR_GROBID_DIR = BASE_DIR