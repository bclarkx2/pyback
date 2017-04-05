
##############################################################################
# Imports                                                                    #
##############################################################################


class User(object):

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


class SimpleUser(User):

    def __init__(self,
                 id,
                 save_locations=[],
                 data_locations=[]):

        self.id = id
        self.save_locations = save_locations
        self.data_locations = data_locations

    def get_id(self):
        return self.id

    def get_save_locations(self):
        return self.save_locations

    def get_data_locations(self):
        return self.data_locations
