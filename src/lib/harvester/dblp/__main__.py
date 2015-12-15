import os.path

import config
from ..common.Harvester import get_arguments
from .DblpDatabaseDownloader import DblpDatabaseDownloader
from .DblpHarvester import DblpHarvester

DBLP_DIR = os.path.join(config.DOWNLOAD_DIR, 'harvester', 'dblp')


if __name__ == '__main__':
    #downloader = DblpDatabaseDownloader(DBLP_DIR)
    #downloader.download()
    limit, _ = get_arguments()

    harvester = DblpHarvester(limit=limit)
    harvester.harvest(os.path.join(DBLP_DIR, 'dblp.xml'))
