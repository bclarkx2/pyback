
##############################################################################
# Imports                                                                    #
##############################################################################

import unittest

from client.datalocation import SimpleDataLocation


##############################################################################
# Constants                                                                  #
##############################################################################

my_name_1 = "my_name_1"
my_path_1 = "my_path_1"


##############################################################################
# TestCases                                                                  #
##############################################################################

class SimpleDataLocationTestCase(unittest.TestCase):

    def setUp(self):
        self.data_location_1 = SimpleDataLocation(my_name_1, my_path_1)

    def test_getters_and_setters(self):

        self.assertEqual(my_name_1, self.data_location_1.get_name())
        self.assertEqual(my_path_1, self.data_location_1.get_path())


if __name__ == '__main__':
    unittest.main()
