import sys

from ..common.Harvester import get_arguments
from .ArxivHarvester import ArxivHarvester


if __name__ == '__main__':
    kwargs = get_arguments(sys.argv[1:])

    harvester = ArxivHarvester()
    harvester.harvest(**kwargs)
