
##############################################################################
# Imports                                                                    #
##############################################################################

import unittest
import json

from client.datalocation import SimpleDataLocation

from utests.commontest import NotSerializable

##############################################################################
# Constants                                                                  #
##############################################################################

my_id_1 = 10
my_name_1 = "my_name_1"
my_path_1 = "my_path_1"


##############################################################################
# TestCases                                                                  #
##############################################################################

class SimpleDataLocationTestCase(unittest.TestCase):

    def setUp(self):
        self.data_location_1 = SimpleDataLocation(my_id_1,
                                                  my_name_1,
                                                  my_path_1)

    def test_getters_and_setters(self):

        self.assertEqual(my_id_1, self.data_location_1.get_id())
        self.assertEqual(my_name_1, self.data_location_1.get_name())
        self.assertEqual(my_path_1, self.data_location_1.get_path())

    #
    # Test: savable
    # # # # # # # # # # # #

    def test_encode_simple_data(self):

        encoder = self.data_location_1.encoder()

        actual_json_str = json.dumps(self.data_location_1, cls=encoder)

        expected_json_str = json.dumps({
            "id": my_id_1,
            "name": my_name_1,
            "path": my_path_1
        })

        self.assertEqual(expected_json_str, actual_json_str)

    def test_encode_serializable(self):
        """should act the same as normal JSON encode"""

        encoder = self.data_location_1.encoder()

        random_dict = {
            "key": "value"
        }

        actual_json_str = json.dumps(random_dict, cls=encoder)

        expected_json_str = json.dumps(random_dict)

        self.assertEqual(expected_json_str, actual_json_str)

    def test_encode_non_simple_data_nonserializable(self):
        """should act the same as normal JSON encode"""

        encoder = self.data_location_1.encoder()

        random_not_serializable = NotSerializable("arg")

        with self.assertRaises(TypeError):
            json.dumps(random_not_serializable, cls=encoder)

    def test_decode_simple_data(self):

        decoder = self.data_location_1.decoder()

        input_dict = {
            "id": my_id_1,
            "name": my_name_1,
            "path": my_path_1
        }
        input_json_obj = json.dumps(input_dict)

        actual_obj = json.loads(input_json_obj, cls=decoder)

        self.assertIsInstance(actual_obj, SimpleDataLocation)
        self.assertEqual(input_dict, actual_obj.to_dict())

    def test_decode_non_local_save_nonserializable(self):
        """should act the same as normal JSON encode"""

        decoder = self.data_location_1.decoder()

        bad_syntax = "{'key'; 'value'}"

        with self.assertRaises(json.decoder.JSONDecodeError):
            json.loads(bad_syntax, cls=decoder)

    def test_decode_non_local_save_serializable(self):

        decoder = self.data_location_1.decoder()

        input_dict = {
            "key": "value"
        }
        input_json_obj = json.dumps(input_dict)

        actual_obj = json.loads(input_json_obj, cls=decoder)

        self.assertNotIsInstance(actual_obj, SimpleDataLocation)
        self.assertIsInstance(actual_obj, dict)


if __name__ == '__main__':
    unittest.main()
