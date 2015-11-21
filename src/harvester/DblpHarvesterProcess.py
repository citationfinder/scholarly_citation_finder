
from process_manager.Process import HarvesterProcess, ProcessError
from process_manager.utils import external_process,external_process2
import subprocess32 as subprocess

import logging
logger = logging.getLogger()

class DblpHarvesterProcess(HarvesterProcess):
    
    PATH = 'scf_lib.harvester.dblp.DblpHarvester'
    PARAM = '-l 100000'
    
    def harvest(self, config = None):
        external_process2(['python', '-m', self.PATH, self.PARAM])

    """
    def harvest(self, config = None):
        try:
            status, stdout, stderr = external_process2(['python', '-m', self.PATH, self.PARAM])
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
    """
