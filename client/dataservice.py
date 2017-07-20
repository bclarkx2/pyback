
###############################################################################
# Imports                                                                     #
###############################################################################

import pickle


###############################################################################
# Class definitions                                                           #
###############################################################################

class DataService(object):
    """docstring for DataService"""
    def __init__(self):
        super(NaiveDataService, self).__init__()

    def get_user(self, user_id):
        raise NotImplementedError("Implement in subclass, please")

    def add_user(self, user):
        raise NotImplementedError("Implement in subclass, please")

    def remove_user(user_id):
        raise NotImplementedError("Implement in subclass, please")

    def save(self):
        raise NotImplementedError("Implement in subclass, please")


class NaiveDataService(object):
    """Naive implementation of the DataService contract

    The idea here is that each function is just done haphazardly. Later, I'll
    come up with a more intelligent implementation.
    """

    def __init__(self, config_filepath):
        super(NaiveDataService, self).__init__()
        self.config_filepath = config_filepath

        self.users = []

    def get_user(self, user_id):
        for user in self.users:
            if user.get_id() == user_id:
                return user
        raise ValueError("user with id {} not found".format(user_id))

    def add_user(self, user):
        if not self.users:
            self.users.append(user)
            return True

        for idx, existing_user in enumerate(self.users):
            if existing_user.get_id() >= user.get_id():
                break
        self.users.insert(idx, user)

    def remove_user(self, user_id):
        for idx, user in enumerate(self.users):
            if user.get_id() == user_id:
                self.users.pop(idx)
                return True
        return False

    def save(self):
        with open(self.config_filepath, 'wb') as save_file:
            pickle.dump(self, save_file)

    @staticmethod
    def from_file(config_filepath):
        try:
            with open(config_filepath, 'rb') as config_file:
                return pickle.load(config_file)
        except pickle.UnpicklingError:
            return NaiveDataService.new_data_service(config_filepath)

    @staticmethod
    def new_data_service(config_filepath):
        return NaiveDataService(config_filepath)

###############################################################################
# Helper functions                                                            #
###############################################################################
