from DblpHarvester import DblpHarvester
from tests import DblpHarvesterTest

if __name__ == '__main__':
    harvester = DblpHarvester()
    harvester.harvest(filename=DblpHarvesterTest.TEST_XML)
