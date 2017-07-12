
##############################################################################
# Imports                                                                    #
##############################################################################

from client.savable import Savable, CustomSavable
from client.savelocation import LocalSaveLocation
from client.datalocation import SimpleDataLocation


##############################################################################
# Base class                                                                 #
##############################################################################

class User(Savable):  # pragma: no cover

    def __init__(self,
                 id,
                 save_locations=[],
                 data_locations=[]):
        raise NotImplementedError("Implement Me!")

    def get_id(self):
        raise NotImplementedError("Implement Me!")

    def get_data_locations(self):
        raise NotImplementedError("Implement Me!")

    def add_data_location(self, data_location):
        raise NotImplementedError("Implement Me!")

    def remove_data_location(self, data_location_id):
        raise NotImplementedError("Implement Me!")

    def get_save_locations(self):
        raise NotImplementedError("Implement Me!")

    def add_save_location(self, save_location):
        raise NotImplementedError("Implement Me!")

    def remove_save_location(self, save_location_id):
        raise NotImplementedError("Implement Me!")

    def backup(self, data_locations, save_locations):
        raise NotImplementedError("Implement Me!")


class SimpleUser(User, CustomSavable):

    def __init__(self,
                 id,
                 save_locations=[],
                 data_locations=[]):

        self.id = id
        self.save_locations = save_locations
        self.data_locations = data_locations

    #
    # Get/set
    # # # # # # # # # # # #

    def get_id(self):
        return self.id

    def get_data_locations(self):
        return self.data_locations

    def add_data_location(self, data_location):
        self.data_locations.append(data_location)

    def remove_data_location(self, data_location_id):
        SimpleUser.remove_by_attr(self.data_locations,
                                  "get_id",
                                  data_location_id)

    def get_save_locations(self):
        return self.save_locations

    def add_save_location(self, save_location):
        self.save_locations.append(save_location)

    def remove_save_location(self, save_location_id):
        SimpleUser.remove_by_attr(self.save_locations,
                                  "get_id",
                                  save_location_id)

    #
    # Meat
    # # # # # # # # # # # #

    def backup(self, data_locations, save_locations):
        pass

    #
    # Utility
    # # # # # # # # # # # #

    @staticmethod
    def remove_by_attr(lst, func_name, remove_this_attr):
        for item in lst:
            attr_method = getattr(item, func_name)
            if attr_method() == remove_this_attr:
                lst.remove(item)

