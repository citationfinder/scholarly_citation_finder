import os.path

import config
from .DblpDatabaseDownloader import DblpDatabaseDownloader
from .DblpHarvester import DblpHarvester

DBLP_DIR = os.path.join(config.DOWNLOAD_DIR, 'harvester', 'dblp')


if __name__ == '__main__':
    #downloader = DblpDatabaseDownloader(DBLP_DIR)
    #downloader.download()
    harvester = DblpHarvester()
    harvester.harvest(os.path.join(DBLP_DIR, 'dblp.xml'))
