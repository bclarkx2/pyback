
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

    def __init__(self):
        raise NotImplementedError("Implement Me!")


##############################################################################
# Implementations                                                            #
##############################################################################

# class LocalSaveLocation(SaveLocation, DefaultSavable):
class LocalSaveLocation(SaveLocation, CustomSavable):

    def __init__(self, save_path):
        self.save_path = save_path

    #
    # Get/set
    # # # # # # # # # # # #

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
            "save_path": self.get_save_path()
        }

    def make_from_dict(self, input_dict):

        # must validate dict before making object
        assert self.validate_dict(input_dict)

        save_path = input_dict['save_path']
        local_save = LocalSaveLocation(save_path)

        return local_save

    def validate_dict(self, input_dict):

        has_save_path = "save_path" in input_dict

        is_local_save = has_save_path

        return is_local_save

    #
    # Static helpers
    # # # # # # # # # # # #

    @staticmethod
    def safe_copy(source_path, dest_path):

        shutil.rmtree(dest_path)
        if(os.path.isdir(source_path)):
            shutil.copytree(source_path, dest_path)
