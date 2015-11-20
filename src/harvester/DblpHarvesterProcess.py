
from process_manager.Process import HarvesterProcess, ProcessError
from process_manager.utils import external_process
import subprocess32 as subprocess

class DblpHarvesterProcess(HarvesterProcess):
    
    PATH = 'harvester.dblp.DblpHarvester'
    
    def harvest(self, config = None):
        try:
            status, stdout, stderr = external_process(['python', '-m', self.PATH])
        except subprocess.TimeoutExpired as e:
            raise ProcessError('DblpHarvester timed out while processing document')
        finally:
            pass
    
        if status != 0:
            raise ProcessError('ParsCit Failure. Possible error:\n' + stderr)
    
        return True