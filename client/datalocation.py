
##############################################################################
# Imports                                                                    #
##############################################################################

import os


##############################################################################
# Base class                                                                 #
##############################################################################

class DataLocation(object):  # pragma: no cover

    def __init__(self, id=None, name="", path=""):
        raise NotImplementedError("Implement Me!")

    def get_id():
        raise NotImplementedError("Implement Me!")

    def get_name():
        raise NotImplementedError("Implement Me!")

    def get_path():
        raise NotImplementedError("Implement Me!")

    @staticmethod
    def new_data_location(id, name, path):
        raise NotImplementedError("Implement Me!")


##############################################################################
# Implementations                                                            #
##############################################################################

class SimpleDataLocation(DataLocation):

    def __init__(self, id=None, name="", path=""):
        self.id = id
        self.name = name
        self.path = path

    #
    # Get/set
    # # # # # # # # # # # #

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path

    @staticmethod
    def new_data_location(id, name, path):

        if not os.path.isdir(path):
            no_dir_err = FileNotFoundError("Could not find data path!")
            no_dir_err.missing_data_path = path
            raise no_dir_err

        return SimpleDataLocation(id, name, path)
