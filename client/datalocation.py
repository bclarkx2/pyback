
##############################################################################
# Imports                                                                    #
##############################################################################



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
