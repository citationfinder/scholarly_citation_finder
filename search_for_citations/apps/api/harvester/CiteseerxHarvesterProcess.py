from ...core.process_manager.Process import HarvesterProcess
from ...core.process_manager.utils import external_process2


class CiteseerxHarvesterProcess(HarvesterProcess):

    PATH = 'search_for_citations.lib.harvester.citeseerx'

    def harvest(self, params):
        process_args = ['python', '-m', self.PATH]
        for key, value in params.iteritems():
            if value:
                process_args.append('--{}'.format(key))
                process_args.append('{}'.format(value))
        external_process2(process_args)
        return process_args