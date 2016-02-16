#import sys

#from ..Harvester import get_arguments
from CiteseerxHarvester import CiteseerxHarvester


if __name__ == '__main__':
    #kwargs = get_arguments(sys.argv[1:])
    #harvester = ArxivHarvester()
    #harvester.harvest(**kwargs)
    #kwargs = get_arguments(sys.argv[1:])

    harvester = CiteseerxHarvester()
    print(harvester.harvest(_from='2008-01-01', until='2008-12-31'))
