from OaiHarvester import OaiHarvester


class ArxivHarvester(OaiHarvester):
    
    def __init__(self, **kwargs):
        # TODO: same database issue
        pass
        #super(ArxivHarvester, self).__init__('arxiv',
        #                                     oai_url='http://export.arxiv.org/oai2',
        #                                     oai_identifier='oai:arXiv.org:',
        #                                     **kwargs)
        # http://arxiv.org/pdf/{id}.pdf