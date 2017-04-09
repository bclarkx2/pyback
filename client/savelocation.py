
##############################################################################
# Imports                                                                    #
##############################################################################

import os
import shutil
import json

from client.savable import Savable, DefaultSavable, CustomSavable


##############################################################################
# Base class                                                                 #
##############################################################################

class SaveLocation(Savable):  # pragma: no cover

    def __init__(self, id=None):
        raise NotImplementedError("Implement Me!")


##############################################################################
# Implementations                                                            #
##############################################################################

# class LocalSaveLocation(SaveLocation, DefaultSavable):
class LocalSaveLocation(SaveLocation, CustomSavable):

    def __init__(self, id=None, save_path=""):
        self.id = id
        self.save_path = save_path

    #
    # Get/set
    # # # # # # # # # # # #

    def get_id(self):
        return self.id

    def get_save_path(self):
        return self.save_path

    #
    # Meat
    # # # # # # # # # # # #

    def save(self, data_location):

        source_path = data_location.get_path()
        dest_name = data_location.get_name()
        dest_path = os.path.join(self.get_save_path(), dest_name)

        LocalSaveLocation.safe_copy(source_path, dest_path)

    #
    # Savable
    # # # # # # # # # # # #

    def to_dict(self):
        return {
            "id": self.get_id(),
            "save_path": self.get_save_path()
        }

    @staticmethod
    def make_from_dict(input_dict):

        # must validate dict before making object
        assert LocalSaveLocation.validate_dict(input_dict)

        id = input_dict['id']
        save_path = input_dict['save_path']
        local_save = LocalSaveLocation(id, save_path)

        return local_save

    @staticmethod
    def validate_dict(input_dict):

        required_fields = ['id', 'save_path']

        has_fields = all(field in input_dict for field in required_fields)

        is_local_save = has_fields

        return is_local_save

    #
    # Static helpers
    # # # # # # # # # # # #

    @staticmethod
    def safe_copy(source_path, dest_path):

        shutil.rmtree(dest_path)
        if(os.path.isdir(source_path)):
            shutil.copytree(source_path, dest_path)
