
###############################################################################
# Imports                                                                     #
###############################################################################


###############################################################################
# Class definitions                                                           #
###############################################################################

class Session(object):
    '''Abstract base for a program session.

    This class contains operations that are
    common for all methods of interacting with the pyback program. These are
    primarily methods for beginning and ending the interaction.
    '''

    def __init__(self, data_service):
        self.data_service = data_service

    def save(self):
        raise NotImplementedError("Implement this, man")


class UserSession(object):
    """Abstract base for a session intended for a single user"""

    def __init__(self, data_service, user_id):
        super(UserSession, self).__init__(data_service)
        self.user = data_service.get_user(user_id)

    def add_save_location(self, save_location):
        raise NotImplementedError("Implement in subclass OR ELSE")

    def add_data_location(self, data_location):
        raise NotImplementedError("Implement in subclass OR ELSE")

    def remove_save_location(self, save_location_id):
        raise NotImplementedError("Implement in subclass OR ELSE")

    def remove_data_location(self, data_location_id):
        raise NotImplementedError("Implement in subclass OR ELSE")

    def backup(self):
        raise NotImplementedError("Implement in subclass OR ELSE")


class SimpleUserSession(object):
    """straightforward session implementation for single user

    This class simply implements a session for a single user. It provides all
    the actions that a user would wish to perform while using the program,
    as well as methods to start and stop the session. It is meant for a single
    user, different sessions may be more appropriate
    """
    def __init__(self, data_service, user_id):
        super(SimpleUserSession, self).__init__(data_service, user_id)

    def add_save_location(self, save_location):
        self.user.add_save_location(save_location)

    def add_data_location(self, data_location):
        self.user.add_data_location(data_location)

    def remove_save_location(self, save_location_id):
        self.user.remove_save_location(save_location_id)

    def remove_data_location(self, data_location_id):
        self.user.remove_data_location(data_location_id)

    def backup(self):
        self.user.backup()

    def save(self):
        self.data_service.save()
