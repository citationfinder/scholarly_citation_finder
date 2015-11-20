
from process_manager.Process import HarvesterProcess, ProcessError
from process_manager.utils import external_process
import subprocess32 as subprocess

import logging
logger = logging.getLogger()

class DblpHarvesterProcess(HarvesterProcess):
    
    PATH = 'scf_lib.harvester.dblp.DblpHarvester'
    
    def harvest(self, config = None):
        try:
            status, stdout, stderr = external_process(['python', '-m', self.PATH])
        except subprocess.TimeoutExpired as e:
            raise ProcessError('DblpHarvester timed out while processing document')
        finally:
            # e.g. delte temp files
            pass
    
        logger.debug('status={}'.format(status))
        logger.debug('stdout={}'.format(stdout))
        logger.debug('stderr={}'.format(stderr))
        
        #if status != 0:
        #    raise ProcessError('DblpHarvester Failure. Possible error:\n' + stderr)
    
        return True
