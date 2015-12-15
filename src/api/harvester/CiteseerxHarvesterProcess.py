import config
from core.process_manager.Process import HarvesterProcess
from core.process_manager.utils import external_process2


class CiteseerxHarvesterProcess(HarvesterProcess):

    PATH = 'lib.harvester.citeseerx'

    def harvest(self, limit=None, _from=None):
        process_args = ['python', '-m', self.PATH]
        if limit:
            process_args.append('-l {}'.format(limit))
        if _from:
            process_args.append('-f {}'.format(_from))
    
        external_process2(process_args, cwd=config.HARVESTER_CITESEERX_DIR)
