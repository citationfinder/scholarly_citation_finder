from nameparser import HumanName


class AuthorNameParser(HumanName):
    
    def __init__(self, full_name='', normalize=False, **kwargs):
        if normalize:
            full_name = full_name.lower().replace('.', '')
        super(AuthorNameParser, self).__init__(full_name=full_name, **kwargs)
