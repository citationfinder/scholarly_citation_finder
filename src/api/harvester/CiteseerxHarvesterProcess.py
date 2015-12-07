
from core.process_manager.Process import HarvesterProcess
from core.process_manager.utils import external_process2

class CiteseerxHarvesterProcess(HarvesterProcess):
    
    PATH = "lib.harvester.citeseer"
    PARAM = '-l 100000'
    
    def harvest(self, config = None):
        external_process2(['python', '-m', self.PATH, self.PARAM])    