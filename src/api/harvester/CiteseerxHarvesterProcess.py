
from core.process_manager.Process import HarvesterProcess
from core.process_manager.utils import external_process2


class CiteseerxHarvesterProcess(HarvesterProcess):

    PATH = 'lib.harvester.citeseerx'

    def harvest(self, limit=None):
        params = ''
        if limit:
            params += '-l {}'.format(limit)
    
        external_process2(['python', '-m', self.PATH, params])
