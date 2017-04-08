
##############################################################################
# Imports                                                                    #
##############################################################################



##############################################################################
# Base class                                                                 #
##############################################################################

class DataLocation(object):  # pragma: no cover

    def __init__(self, name="", path=""):
        raise NotImplementedError("Implement Me!")

    def get_name():
        raise NotImplementedError("Implement Me!")

    def get_path():
        raise NotImplementedError("Implement Me!")


class SimpleDataLocation(DataLocation):

    def __init__(self, name="", path=""):
        self.name = name
        self.path = path

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path
