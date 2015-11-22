import unittest

from lib.harvester.common import HarvesterTest
from lib.harvester.dblp import DblpHarvesterTest

from lib import ParserTest
from lib.extractor.common import ExtractorTest
from lib.extractor.grobid import GrobidExtractorTest

tests = unittest.TestLoader()
test_arr = []
#test_arr.append(tests.loadTestsFromModule(HarvesterTest))
#test_arr.append(tests.loadTestsFromModule(DblpHarvesterTest))
#test_arr.append(tests.loadTestsFromModule(ExtractorTest))
#test_arr.append(tests.loadTestsFromModule(ParserTest))
test_arr.append(tests.loadTestsFromModule(GrobidExtractorTest))

all_tests = unittest.TestSuite(test_arr)

if __name__ == '__main__':
    unittest.TextTestRunner().run(all_tests)