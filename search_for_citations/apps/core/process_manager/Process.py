from .utils import external_process2

class Process(object):
    
    def run(self, process_args, process_args_additional=None):
        if process_args_additional:
            for key, value in process_args_additional.iteritems():
                if value:
                    process_args.append('--{}'.format(key))
                    process_args.append('{}'.format(value))
          
        external_process2(process_args)
        return process_args

    """
    def log(self, msg):
        self.logger.info('{0} for run {1}: {2}'.format(self.__class__.__name__, self.run_name, msg))

    def run(self, config):
        try:
            if isinstance(self, HarvesterProcess):
                return self.harvest(config)
            elif isinstance(self, ExtractorProcess):
                return self.extract(config)
        except ProcessError as r:
            return r
        except Exception as e:
            #e_info = sys.exc_info()
            #self.log(''.join(traceback.format_exception(*e_info)))
            return ProcessError('{0}: {1}'.format(e.__class__.__name__, e))
    """


class HarvesterProcess(Process):
    pass
    #def harvest(self, params):
    #    raise ProcessError('Override this method')


class ExtractorProcess(Process):
    pass


class ProcessError(Exception):
    pass
