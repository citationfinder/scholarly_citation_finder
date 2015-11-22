import unittest

from lib.harvester.common import HarvesterTest
from lib.harvester.dblp import DblpHarvesterTest

from lib import ParserTest
from lib.extractor.common import ExtractorTest
from lib.extractor.grobid import GrobidExtractorTest
from lib.extractor.citeseer import CiteseerExtractorTest

CiteseerExtractorTest = unittest.TestLoader()
test_arr = []
#test_arr.append(CiteseerExtractorTest.loadTestsFromModule(HarvesterTest))
#test_arr.append(CiteseerExtractorTest.loadTestsFromModule(DblpHarvesterTest))
#test_arr.append(CiteseerExtractorTest.loadTestsFromModule(ExtractorTest))
#test_arr.append(CiteseerExtractorTest.loadTestsFromModule(ParserTest))
#test_arr.append(CiteseerExtractorTest.loadTestsFromModule(GrobidExtractorTest))
test_arr.append(CiteseerExtractorTest.loadTestsFromModule(CiteseerExtractorTest))

all_tests = unittest.TestSuite(test_arr)

if __name__ == '__main__':
    unittest.TextTestRunner().run(all_tests)