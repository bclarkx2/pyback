
##############################################################################
# Imports                                                                    #
##############################################################################

import unittest
import pickle

from unittest.mock import MagicMock

import client
from client.dataservice import NaiveDataService

from utests import commontest


class NaiveDataServiceTestCase(unittest.TestCase):

    def setUp(self):
        pass

    #
    # Test: init
    # # # # # # # # # # # #

    def test_init(self):
        service = NaiveDataService("/path/to/config_file.json")
        self.assertEqual("/path/to/config_file.json", service.config_filepath)


if __name__ == '__main__':
    unittest.main()
