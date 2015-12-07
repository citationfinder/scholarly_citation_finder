from core.process_manager.Process import HarvesterProcess
from core.process_manager.utils import external_process2


class ArxivHarvesterProcess(HarvesterProcess):
    
    PATH = "lib.harvester.arxiv"
    PARAM = '-l 10'
    
    def harvest(self, config = None):
        external_process2(['python', '-m', self.PATH, self.PARAM])    