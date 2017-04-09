
##############################################################################
# Imports                                                                    #
##############################################################################

import json

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

    #
    # Savable
    # # # # # # # # # # # #

    def to_dict(self):
        self_dict = {}

        self_dict['id'] = self.get_id()

        save_locations_arr = []
        for save_location in self.get_save_locations():
            cur_save_dict = save_location.to_dict()
            save_locations_arr.append(cur_save_dict)
        self_dict['save_locations'] = save_locations_arr

        data_locations_arr = []
        for data_location in self.get_data_locations():
            cur_data_dict = data_location.to_dict()
            data_locations_arr.append(cur_data_dict)
        self_dict['data_locations'] = data_locations_arr

        return self_dict

    @staticmethod
    def make_from_dict(input_dict):

        assert SimpleUser.validate_dict(input_dict)

        id = input_dict['id']

        save_locations_arr = []
        cat_save_locations_json = input_dict['save_locations']
        for save_json in cat_save_locations_json:

            # ideal code
            # save_obj = json.loads(save_json, cls=SaveLocation.decoder())
            # if isinstance(save_obj, SaveLocation):
            #     save_locations_arr.append(save_obj)

            if LocalSaveLocation.validate_dict(save_json):
                save_obj = LocalSaveLocation.make_from_dict(input_dict)
                save_locations_arr.append(save_obj)

        data_locations_arr = []
        cat_data_locations_json = input_dict['data_locations']
        for data_json in cat_data_locations_json:

            # ideal code
            # data_obj = json.loads(data_json, cls=DataLocation.decoder())
            # if isinstance(data_obj, DataLocation):
            #     data_locations_arr.append(data_obj)

            if SimpleDataLocation.validate_dict(data_json):
                data_obj = SimpleDataLocation.make_from_dict(input_dict)
                data_locations_arr.append(data_obj)

        simple_user = SimpleUser(id,
                                 save_locations_arr,
                                 data_locations_arr)
        return simple_user

    @staticmethod
    def validate_dict(input_dict):

        required_fields = ['id', 'save_locations', 'data_locations']

        has_req_fields = all(field in input_dict for field in required_fields)

        is_valid_dict = has_req_fields

        return is_valid_dict
