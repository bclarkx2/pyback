
##############################################################################
# Imports                                                                    #
##############################################################################

import os
import shutil
import json

from client.savable import Savable, DefaultSavable


##############################################################################
# Base class                                                                 #
##############################################################################

class SaveLocation(Savable):  # pragma: no cover

    def __init__(self):
        raise NotImplementedError("Implement Me!")


##############################################################################
# Implementations                                                            #
##############################################################################

class LocalSaveLocation(SaveLocation, DefaultSavable):

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

    def encoder(self):
        return LocalSaveLocation.LocalSaveEncoder

    def decoder(self):
        return LocalSaveLocation.LocalSaveDecoder

    class LocalSaveEncoder(json.JSONEncoder):

        def default(self, o):

            if isinstance(o, LocalSaveLocation):
                return {
                    "save_path": o.get_save_path()
                }
            else:
                return json.JSONEncoder.default(self, o)

    class LocalSaveDecoder(json.JSONDecoder):

        def __init__(self):
            json.JSONDecoder.__init__(self, object_hook=self.decode)

        def decode(self, incoming_str):

            incoming_dict = json.loads(incoming_str)

            is_local_save = self.is_dict_local_save(incoming_dict)

            if is_local_save:
                save_path = incoming_dict['save_path']
                local_save = LocalSaveLocation(save_path)
                return local_save
            else:
                return incoming_dict

        def is_dict_local_save(self, incoming_dict):

            has_save_path = "save_path" in incoming_dict

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
