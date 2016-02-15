#import sys

#from ..Harvester import get_arguments
from CiteseerxHarvester import CiteseerxHarvester


if __name__ == '__main__':
    #kwargs = get_arguments(sys.argv[1:])

    harvester = CiteseerxHarvester()
    print(harvester.harvest(_from='2008-07-01', until='2008-12-31', _from_id='10.1.1.101.8510'))
