import os.path
import sys

from search_for_citations import config
from ..Harvester import get_arguments
from .DblpDatabaseDownloader import DblpDatabaseDownloader
from .DblpHarvester import DblpHarvester

DBLP_DIR = os.path.join(config.DOWNLOAD_DIR, 'harvester', 'dblp')


if __name__ == '__main__':
    #downloader = DblpDatabaseDownloader(DBLP_DIR)
    #downloader.download()
    kwargs = get_arguments(sys.argv[1:])

    harvester = DblpHarvester()
    harvester.harvest(filename=os.path.join(DBLP_DIR, 'dblp.xml'), **kwargs)
