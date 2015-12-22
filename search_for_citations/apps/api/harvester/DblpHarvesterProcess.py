from ...core.process_manager.Process import HarvesterProcess
from ...core.process_manager.utils import external_process2


class DblpHarvesterProcess(HarvesterProcess):

    PATH = 'search_for_citations.lib.harvester.dblp'

    def harvest(self, params):
        process_args = ['python', '-m', self.PATH]
        for key, value in params.iteritems():
            if value:
                process_args.append('--{} {}'.format(key))
                process_args.append('{}'.format(value))
        external_process2(process_args)
        return process_args

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
