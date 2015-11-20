from ..Process import external_process, ProcessError
from ..utils import external_pr

import subprocess32 as subprocess

class DblpHarvesterProcess(HarvesterProcess):
    
    def harvest(self):
        
        try:
            status, stoud, sterr = external_process(['python', '-m', 'harvester.dblp.DblpHarvester'])
        except subprocess.TimeoutExpired as e:
            raise ProcessError('DblpHarvester timed out while processing')
        finally:
            pass
        
        if status != 0:
            raise ProcessError('DblpHarvester Failure. Error:\n' + stderr)
        
        # May something else
        return True;