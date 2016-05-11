
class Strategy(object):
    '''
    Abstract strategy class.
    '''
    
    name = None
    logger = None
    database = None
    
    def __init__(self, name):
        '''
        Create object.
        
        :param name: Strategy name
        '''
        self.name = name
    
    def setup(self, database):
        '''
        Setup strategy object.
        
        :param database: Database name
        '''
        self.database = database
    
    def run(self, publication_set, callback):
        '''
        Run the strategy.
        
        :param publication_set: Publication set
        :param callback: Callback method
        '''
        raise Exception('Implement this method')
