
##############################################################################
# Imports                                                                    #
##############################################################################

import os
import shutil


##############################################################################
# Base class                                                                 #
##############################################################################

class SaveLocation(object):  # pragma: no cover

    def __init__(self):
        raise NotImplementedError("Implement Me!")


##############################################################################
# Implementations                                                            #
##############################################################################

class LocalSaveLocation(SaveLocation):

    def __init__(self, save_path):
        self.save_path = save_path

    def get_save_path(self):
        return self.save_path

    def save(self, data_location):

        source_path = data_location.get_path()
        dest_name = data_location.get_name()
        dest_path = os.path.join(self.get_save_path(), dest_name)

        LocalSaveLocation.safe_copy(source_path, dest_path)

    @staticmethod
    def safe_copy(source_path, dest_path):

        shutil.rmtree(dest_path)
        if(os.path.isdir(source_path)):
            shutil.copytree(source_path, dest_path)
