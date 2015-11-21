import unittest

from scf_lib.harvester.common import HarvesterTest
from scf_lib.harvester.dblp import DblpHarvesterTest

from scf_lib.extractor import ExtractorTest

tests = unittest.TestLoader()
test_arr = []
#test_arr.append(tests.loadTestsFromModule(HarvesterTest))
#test_arr.append(tests.loadTestsFromModule(DblpHarvesterTest))
test_arr.append(tests.loadTestsFromModule(ExtractorTest))

all_tests = unittest.TestSuite(test_arr)

if __name__ == '__main__':
    unittest.TextTestRunner().run(all_tests)