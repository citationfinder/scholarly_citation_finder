import unittest

from harvester.common import HarvesterTest
from harvester.dblp import DblpHarvesterTest

tests = unittest.TestLoader()
test_arr = []
test_arr.append(tests.loadTestsFromModule(HarvesterTest))
test_arr.append(tests.loadTestsFromModule(DblpHarvesterTest))

all_tests = unittest.TestSuite(test_arr)

if __name__ == '__main__':
    unittest.TextTestRunner().run(all_tests)