import config
from core.process_manager.Process import HarvesterProcess
from core.process_manager.utils import external_process2


class DblpHarvesterProcess(HarvesterProcess):

    PATH = 'lib.harvester.dblp'

    def harvest(self, limit=None):
        process_args = ['python', '-m', self.PATH]
        if limit:
            process_args.append('-l {}'.format(limit))

        external_process2(process_args, cwd=config.HARVESTER_DBLP_DIR)

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
