
##############################################################################
# Imports                                                                    #
##############################################################################

import unittest
import os
import json

from client.savelocation import LocalSaveLocation

from unittest.mock import MagicMock, call, patch

from utests.commontest import MultiPatch


##############################################################################
# Constants                                                                  #
##############################################################################

id_1 = 11
name_1 = "name_1"
save_path_1 = "/some/save/path"
save_item = os.path.join(save_path_1, name_1)

data_path_1 = "/some/data/path/pre_save_name_1"


##############################################################################
# TestCases                                                                  #
##############################################################################

class LocalSaveLocationTestCase(unittest.TestCase):

    def setUp(self):
        self.save_location_1 = LocalSaveLocation(id_1, save_path_1)

    def test_getters_and_setters(self):

        self.assertEqual(id_1, self.save_location_1.get_id())
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

        with MultiPatch(patches):
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

        with MultiPatch(patches):
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


if __name__ == '__main__':
    unittest.main()
