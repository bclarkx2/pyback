
##############################################################################
# Imports                                                                    #
##############################################################################

import unittest
import os
import json

import client
from client.savelocation import LocalSaveLocation

from unittest.mock import MagicMock, call, patch

from utests import commontest


##############################################################################
# Constants                                                                  #
##############################################################################

name_1 = "name_1"
save_path_1 = "/some/save/path"
save_item = os.path.join(save_path_1, name_1)

data_path_1 = "/some/data/path/pre_save_name_1"


##############################################################################
# TestCases                                                                  #
##############################################################################

class LocalSaveLocationTestCase(unittest.TestCase):

    def setUp(self):
        self.save_location_1 = LocalSaveLocation(save_path_1)

    def test_getters_and_setters(self):

        self.assertEqual(save_path_1, self.save_location_1.get_save_path())

    def test_safe_copy_valid_dir(self):

        shutil_mock = MagicMock()
        path_mock = MagicMock()
        path_mock.isdir.return_value = True

        patches = [
            ("shutil.rmtree",),
            ("shutil.copytree", shutil_mock),
            ("os.path", path_mock)
        ]

        with commontest.MultiPatch(patches):
            LocalSaveLocation.safe_copy(data_path_1, save_item)

        shutil_args = [
            call(data_path_1, save_item)
        ]

        self.assertEqual(shutil_args, shutil_mock.call_args_list)

    def test_safe_copy_invalid_dir(self):

        shutil_mock = MagicMock()
        path_mock = MagicMock()
        path_mock.isdir.return_value = False

        patches = [
            ("shutil.rmtree",),
            ("shutil.copytree", shutil_mock),
            ("os.path", path_mock)
        ]

        with commontest.MultiPatch(patches):
            LocalSaveLocation.safe_copy(data_path_1, save_item)

        shutil_args = []

        self.assertEqual(shutil_args, shutil_mock.call_args_list)

    def test_save_nominal(self):

        safe_copy_mock = MagicMock()

        data_location_mock = MagicMock()
        data_location_mock.get_name.return_value = name_1
        data_location_mock.get_path.return_value = data_path_1

        with patch("client.savelocation.LocalSaveLocation.safe_copy", safe_copy_mock):
            self.save_location_1.save(data_location_mock)

        expected_copy_args = [
            call(data_path_1, save_item)
        ]

        self.assertEqual(expected_copy_args, safe_copy_mock.call_args_list)

    def test_encode_local_save(self):

        encoder = self.save_location_1.encoder()

        actual_json_str = json.dumps(self.save_location_1, cls=encoder)

        expected_json_str = json.dumps({
            "save_path": save_path_1
        })

        self.assertEqual(expected_json_str, actual_json_str)

    def test_encode_serializable(self):
        """should act the same as normal JSON encode"""

        encoder = self.save_location_1.encoder()

        random_dict = {
            "key": "value"
        }

        actual_json_str = json.dumps(random_dict, cls=encoder)

        expected_json_str = json.dumps(random_dict)

        self.assertEqual(expected_json_str, actual_json_str)

    def test_encode_non_local_save_nonserializable(self):
        """should act the same as normal JSON encode"""

        encoder = self.save_location_1.encoder()

        random_not_serializable = NotSerializable("arg")

        with self.assertRaises(TypeError):
            json.dumps(random_not_serializable, cls=encoder)

    def test_decode_local_save(self):

        decoder = self.save_location_1.decoder()

        input_dict = {
            "save_path": "/incoming/path"
        }
        input_json_obj = json.dumps(input_dict)

        actual_obj = json.loads(input_json_obj, cls=decoder)

        self.assertIsInstance(actual_obj, LocalSaveLocation)
        self.assertEqual("/incoming/path", actual_obj.get_save_path())

    def test_decode_non_local_save_nonserializable(self):
        """should act the same as normal JSON encode"""

        decoder = self.save_location_1.decoder()

        bad_syntax = "{'key'; 'value'}"

        with self.assertRaises(json.decoder.JSONDecodeError):
            json.loads(bad_syntax, cls=decoder)

    def test_decode_non_local_save_serializable(self):

        decoder = self.save_location_1.decoder()

        input_dict = {
            "key": "value"
        }
        input_json_obj = json.dumps(input_dict)

        actual_obj = json.loads(input_json_obj, cls=decoder)

        self.assertNotIsInstance(actual_obj, LocalSaveLocation)
        self.assertIsInstance(actual_obj, dict)


class NotSerializable(object):

    def __init__(self, arg):
        self.arg = arg


if __name__ == '__main__':
    unittest.main()
