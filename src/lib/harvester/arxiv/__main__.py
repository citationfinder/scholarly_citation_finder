from ..common.Harvester import get_arguments
from .ArxivHarvester import ArxivHarvester

if __name__ == '__main__':
    limit, _from = get_arguments()

    harvester = ArxivHarvester(limit=limit)
    harvester.harvest(_from=_from)
