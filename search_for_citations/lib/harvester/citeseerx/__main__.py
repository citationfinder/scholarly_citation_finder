import sys

from ..common.Harvester import get_arguments
from .CiteseerxHarvester import CiteseerxHarvester


if __name__ == '__main__':
    kwargs = get_arguments(sys.argv[1:])

    harvester = CiteseerxHarvester()
    harvester.harvest(**kwargs)
