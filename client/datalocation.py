
##############################################################################
# Imports                                                                    #
##############################################################################

from client.savable import Savable, CustomSavable


##############################################################################
# Base class                                                                 #
##############################################################################

class DataLocation(Savable):  # pragma: no cover

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

class SimpleDataLocation(DataLocation, CustomSavable):

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

    #
    # Savable
    # # # # # # # # # # # #

    def to_dict(self):
        return {
            "id": self.get_id(),
            "name": self.get_name(),
            "path": self.get_path()
        }

    @staticmethod
    def make_from_dict(input_dict):

        # must validate dict before making object
        assert SimpleDataLocation.validate_dict(input_dict)

        id = input_dict['id']
        name = input_dict['name']
        path = input_dict['path']

        simple_data_location = SimpleDataLocation(id, name, path)

        return simple_data_location

    @staticmethod
    def validate_dict(input_dict):

        required_fields = ['id', 'name', 'path']

        has_req_fields = all(field in input_dict for field in required_fields)

        is_simple_data_location = has_req_fields

        return is_simple_data_location
