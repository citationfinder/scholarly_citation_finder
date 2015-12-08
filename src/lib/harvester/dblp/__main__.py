import os.path

import config
from .DblpHarvester import DblpHarvester

if __name__ == '__main__':
    harvester = DblpHarvester()
    harvester.harvest(os.path.join(config.DOWNLOAD_DIR, 'dblp', 'dblp.xml'))
