#!/usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

import cmd
import sys
import os
import shutil
import pickle
import json

from copy import deepcopy

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
parent_dir = os.path.dirname(current_dir)

if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from client.dataservice import NaiveDataService
from client.user import SimpleUser
from client.session import SimpleUserSession
from client.datalocation import SimpleDataLocation
from client.savelocation import LocalSaveLocation

from enum import Enum

###############################################################################
# Constants                                                                   #
###############################################################################

missing_data_service_msg = "must select a data service first!"
missing_session_msg = "must start a session first!"


###############################################################################
# Enums                                                                       #
###############################################################################

class State(Enum):
    """Current state of CLI session"""
    UNINITIALIZED = 0
    HAS_DATA = 1
    HAS_SESSION = 2

    def min_err_msg(self):
        if self == State.UNINITIALIZED:
            return "Too initialized"
        elif self == State.HAS_DATA:
            return missing_data_service_msg
        elif self == State.HAS_SESSION:
            return missing_session_msg
        else:
            return "Unidentified state error"

    def exact_err_msg(self):
        if self == State.UNINITIALIZED:
            return "Must not have data service selected"
        elif self == State.HAS_DATA:
            return "Must have data service but not logged in"
        elif self == State.HAS_SESSION:
            return "Must have logged in"
        else:
            return "Unidentified state error"

    def at_least(self, required_state):
        return self.value >= required_state.value

    def exactly(self, required_state):
        return self.value == required_state.value


###############################################################################
# Decorators                                                                  #
###############################################################################

class RequiredState(object):

    def __init__(self, required_state):
        self._required_state = required_state

    def required_state(self):
        return self._required_state

    def shell_in_valid_state(self, shell):
        raise NotImplementedError("AHH")

    def error_msg(self):
        raise NotImplementedError("AHH")

    def __call__(self, operation):
        def wrapped_operation(*args):
            shell = args[0]
            if self.shell_in_valid_state(shell):
                operation(*args)
            else:
                print(self.error_msg())
        return wrapped_operation


class ExactRequiredState(RequiredState):

    def __init__(self, required_state):
        super(ExactRequiredState, self).__init__(required_state)

    def shell_in_valid_state(self, shell):
        return shell.in_exact_state(self.required_state())

    def error_msg(self):
        return self.required_state().exact_err_msg()


class MinimimRequiredState(RequiredState):
    """decorator for requiring a state for an operation"""

    def __init__(self, required_state):
        super(MinimimRequiredState, self).__init__(required_state)

    def shell_in_valid_state(self, shell):
        return shell.in_minimum_required_state(self.required_state())

    def error_msg(self):
        return self.required_state().min_err_msg()


###############################################################################
# Class definitions                                                           #
###############################################################################

class PybackShell(cmd.Cmd):
    """CLI interface for pyback program"""

    intro = "Welcome to pyback! Enter your user ID to begin:"
    prompt = '(pyback) '

    def __init__(self):
        super(PybackShell, self).__init__()
        self.state = State.UNINITIALIZED
        self.data_service = None
        self.session = None

    #
    # Control flow commands
    # # # # # # # # # # # #

    def in_minimum_required_state(self, required_state):
        return self.state.at_least(required_state)

    def in_exact_state(self, required_state):
        return self.state.exactly(required_state)

    def do_quit(self, arg):
        '''exit program'''
        print("see ya, wouldn't want to be ya")
        if self.in_minimum_required_state(State.HAS_SESSION):
            print("saving session!")
            self.session.save()
        sys.exit(0)

    #
    # Data service commands
    # # # # # # # # # # # # #

    def do_new_data_service(self, config_filepath):
        '''start a new data service'''
        print("starting new data_service at {}".format(config_filepath))
        self.data_service = start_new_data_service(config_filepath)
        self.state = State.HAS_DATA

    def do_select_data_service(self, config_filepath):
        '''select an existing data service'''
        try:
            self.data_service = select_data_service(config_filepath)
            self.state = State.HAS_DATA
            print("selected data service!")
        except ValueError as err:
            print(err)

    @MinimimRequiredState(State.HAS_DATA)
    def do_print_data_service(self, arg):
        '''print data service'''
        print(self.data_service)

    #
    # Session starting commands
    # # # # # # # # # # # # # #

    @ExactRequiredState(State.HAS_DATA)
    def do_new_user_login(self, user_id):
        new_user = SimpleUser(user_id)
        self.data_service.add_user(new_user)
        self.do_login(user_id)

    @ExactRequiredState(State.HAS_DATA)
    def do_login(self, user_id):
        if not user_id:
            print("Please specify a user ID")
            return

        if self.data_service.has_user(user_id):
            self.session = SimpleUserSession(self.data_service, user_id)
            self.state = State.HAS_SESSION
            self.prompt = '(pyback[{}]) '.format(user_id)
            print("logged in as {}!".format(user_id))
        else:
            print("User {} does not exist!".format(user_id))

    #
    # Session commands
    # # # # # # # # # # # #

    @MinimimRequiredState(State.HAS_SESSION)
    def do_add_data_location(self, args):

        args = args.split(' ')

        if len(args) != 2:
            print("Please enter dir path and location name")
            return

        name = args[0]
        data_path = os.path.expanduser(args[1])

        try:
            data_location = SimpleDataLocation.new_data_location(id=name,
                                                                 name=name,
                                                                 path=data_path)
            self.session.add_data_location(data_location)
            print("Added data location {}".format(name))
        except FileNotFoundError as err:
            print("{}: {}".format(err, err.missing_data_path))

    @MinimimRequiredState(State.HAS_SESSION)
    def do_remove_data_location(self, data_location_id):
        try:
            self.session.remove_data_location(data_location_id)
        except Exception:
            print("could not remove data location!")

    @MinimimRequiredState(State.HAS_SESSION)
    def do_add_save_location(self, args):

        args = args.split(' ')
        if len(args) != 2:
            print("Enter save name and path")

        name = args[0]
        path = os.path.expanduser(args[1])

        try:
            save_location = LocalSaveLocation.new_save_location(id=name,
                                                                save_path=path)
            self.session.add_save_location(save_location)
            print("Added save location {}".format(name))
        except FileNotFoundError as err:
            print("{}: {}".format(err, err.missing_save_path))

    @MinimimRequiredState(State.HAS_SESSION)
    def do_remove_save_location(self, save_location_id):
        self.session.remove_save_location(save_location_id)

    @MinimimRequiredState(State.HAS_SESSION)
    def do_backup(self, arg):
        self.session.backup()


###############################################################################
# Helper functions                                                            #
###############################################################################

def start_new_data_service(config_filepath):
    config_filepath = os.path.expanduser(config_filepath)

    if os.path.isfile(config_filepath):
        os.remove(config_filepath)

    new_data_service = NaiveDataService.new_data_service(config_filepath)

    with open(config_filepath, 'wb') as config_file:
        pickle.dump(new_data_service, config_file)

    return new_data_service


def select_data_service(config_filepath):
    config_filepath = os.path.expanduser(config_filepath)
    try:
        with open(config_filepath, 'rb') as config_file:
            return pickle.load(config_file)
    except IOError:
        raise ValueError("Could not read file")
    except pickle.UnpicklingError:
        raise ValueError("Could not load data service from filepath")


###############################################################################
# Main script                                                                 #
###############################################################################

if __name__ == '__main__':
    PybackShell().cmdloop()