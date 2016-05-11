from nameparser import HumanName


class AuthorNameParser(HumanName):
    '''
    Split a author name into it's components.
    '''
    
    def __init__(self, full_name='', normalize=False, **kwargs):
        '''
        Create a object.
        
        :param full_name: Full name of the author
        :param normalize: If true, the name gets normalized
        '''
        if normalize:
            full_name = full_name.lower().replace('.', '')
        super(AuthorNameParser, self).__init__(full_name=full_name, **kwargs)
