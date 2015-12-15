from ..common.Harvester import get_arguments
from .CiteseerxHarvester import CiteseerxHarvester

if __name__ == '__main__':
    limit, _from = get_arguments()

    harvester = CiteseerxHarvester(limit=limit)
    harvester.harvest(_from=_from)
