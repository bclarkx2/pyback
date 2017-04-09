
##############################################################################
# Imports                                                                    #
##############################################################################

import unittest
import json

from unittest.mock import MagicMock

import client
from client.user import SimpleUser
from client.savelocation import LocalSaveLocation
from client.datalocation import SimpleDataLocation

from utests import commontest


class SimpleUserTestCase(unittest.TestCase):

    def setUp(self):
        self.empty_user = SimpleUser(100)

    def test_init(self):

        simple_user = SimpleUser(10)
        self.assertEqual(10, simple_user.get_id())

    def test_getters_and_setters(self):

        data_mock = MagicMock()
        a_data_location = MagicMock()
        a_data_location.get_id.return_value = 111
        data_mock.DataLocation.return_value = a_data_location

        save_mock = MagicMock()
        a_save_location = MagicMock()
        a_save_location.get_id.return_value = 222
        save_mock.SaveLocation.return_value = a_save_location

        patches = [
            ("client.savelocation", save_mock),
            ("client.datalocation", data_mock)
        ]

        with commontest.MultiPatch(patches):
            self.empty_user.add_data_location(client.datalocation.DataLocation())
            self.empty_user.add_save_location(client.savelocation.SaveLocation())

            expected_data_locations = [a_data_location]
            actual_data_locations = self.empty_user.get_data_locations()
            self.assertEqual(expected_data_locations, actual_data_locations)

            expected_save_locations = [a_save_location]
            actual_save_locations = self.empty_user.get_save_locations()
            self.assertEqual(expected_save_locations, actual_save_locations)

            self.empty_user.remove_data_location(111)
            expected_data_locations = []
            actual_data_locations = self.empty_user.data_locations
            self.assertEqual(expected_data_locations, actual_data_locations)

            self.empty_user.remove_save_location(222)
            expected_save_locations = []
            actual_save_locations = self.empty_user.save_locations
            self.assertEqual(expected_save_locations, actual_save_locations)

    def test_backup(self):

        self.empty_user.backup(None, None)

    #
    # Savable
    # # # # # # # # # # # #

    def test_basic_savable(self):

        local_save_1 = LocalSaveLocation(22, "/a/save/path")

        simple_data_1 = SimpleDataLocation(33, "a_data_name", "/a/data/path")

        simple_user = SimpleUser(11, [local_save_1], [simple_data_1])

        encoder = simple_user.encoder()

        actual_json_str = json.dumps(simple_user, cls=encoder)

        expected_json_str = json.dumps({
            "id": 11,
            "save_locations": [
                {
                    "id": 22,
                    "save_path": "/a/save/path"
                }
            ],
            "data_locations": [
                {
                    "id": 33,
                    "path": "/a/data/path",
                    "name": "a_data_name"
                }
            ]
        })

        self.assertEqual(expected_json_str, actual_json_str)


if __name__ == '__main__':
    unittest.main()
