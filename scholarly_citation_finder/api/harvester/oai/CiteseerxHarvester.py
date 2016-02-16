from OaiHarvester import OaiHarvester


class CiteseerxHarvester(OaiHarvester):
    
    def __init__(self, **kwargs):
        super(CiteseerxHarvester, self).__init__('citeseerx',
                                                 oai_url='http://citeseerx.ist.psu.edu/oai2',
                                                 oai_identifier='oai:CiteSeerX.psu:',
                                                 **kwargs)
        # http://citeseerx.ist.psu.edu/viewdoc/download?doi={id}&amp;rep=rep1&amp;type=pdf
