import logging
from .Process import HarvesterProcess, ExtractorProcess

class ProcessRunner:
    
    def __init__(self):
        self.harvesterProcesses = []
        self.extractorProcesses = []
        self.processes = []
        
        #self.result_logger = logging.getLogger('result')
        #self.runnable_logger = logging.getLogger('runnables')
        #self.result_logger.setLevel(logging.INFO)
        #self.runnable_logger.setLevel(logging.INFO)
        
    def add_process(self, process, output_results=True):
        self.processes.append(process)

        if issubclass(process, HarvesterProcess):
            self.harvesterProcesses.append(process)
        if issubclass(process, ExtractorProcess):
            self.harvesterProcesses.append(process)
            
            
