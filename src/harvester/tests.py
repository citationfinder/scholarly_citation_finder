from django.test import TestCase
from .DblpHarvesterProcess import DblpHarvesterProcess

class DblpHarvesterProcessTest(TestCase):
    
    def setUp(self):
        self.process = DblpHarvesterProcess()
     
    """   
    def test_harvest(self):
        first = self.process.harvest()
        self.assertEqual(first, True)
    """