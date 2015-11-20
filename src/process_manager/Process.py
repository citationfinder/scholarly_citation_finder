import sys

class Process():
    
    def __init__(self):
        pass

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


class HarvesterProcess(Process):
    def harvest(self, config):
        raise ProcessError('Override this method')
    
class ExtractorProcess(Process):
    def extract(self, config):
        raise ProcessError('Override this method')
    

class ProcessError(Exception):
    
    def __init__(self, msg):
        self.msg = msg
        
    def __unicode__(self):
        return "RunnableError: {0}".format(self.msg)
