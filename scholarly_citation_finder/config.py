import os.path
from settings.base import BASE_DIR


def get_abspath(path):
    return os.path.abspath(os.path.join(BASE_DIR, path))

# Paths
#
TEST_DIR = get_abspath('../test_data')
DOWNLOAD_DIR = get_abspath('../downloads')
DOWNLOAD_TMP_DIR = os.path.join(DOWNLOAD_DIR, 'tmp')
EVALUATION_DIR = os.path.join(DOWNLOAD_DIR, 'evaluation')
LOG_DIR = get_abspath('../log')