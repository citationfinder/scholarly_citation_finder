
class Strategy(object):
    
    name = None
    logger = None
    database = None
    
    def __init__(self, name):
        self.name = name
    
    def setup(self, database):
        self.database = database
    
    def run(self, publication_set, callback):
        raise Exception('Implement this method')
