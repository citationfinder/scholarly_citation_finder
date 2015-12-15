import config
from core.process_manager.Process import HarvesterProcess
from core.process_manager.utils import external_process2


class ArxivHarvesterProcess(HarvesterProcess):

    PATH = 'lib.harvester.arxiv'

    def harvest(self, limit=None):
        params = ''
        if limit:
            params += '-l {}'.format(limit)

        external_process2(['python', '-m', self.PATH, params], cwd=config.HARVESTER_ARXIV_DIR)
