
from ..process_manager.Process import HarvesterProcess, ProcessError
from ..process_manager.utils import external_process,external_process2

class CiteseerxHarvesterProcess(HarvesterProcess):
    
    PATH = "lib.harvester.citeseer.CiteseerxHarvester"
    PARAM = '-l 100000'
    
    def harvest(self, config = None):
        external_process2(['python', '-m', self.PATH, self.PARAM])    