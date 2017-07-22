
##############################################################################
# Imports                                                                    #
##############################################################################

import os
import shutil


##############################################################################
# Base class                                                                 #
##############################################################################

class SaveLocation(object):  # pragma: no cover

    def __init__(self, id=None):
        raise NotImplementedError("Implement Me!")


##############################################################################
# Implementations                                                            #
##############################################################################

# class LocalSaveLocation(SaveLocation, DefaultSavable):
class LocalSaveLocation(SaveLocation):

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
    # Static helpers
    # # # # # # # # # # # #

    @staticmethod
    def safe_copy(source_path, dest_path):

        if os.path.isdir(dest_path):
            shutil.rmtree(dest_path)
        if(os.path.isdir(source_path)):
            shutil.copytree(source_path, dest_path)
