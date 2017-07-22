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


###############################################################################
# Constants                                                                   #
###############################################################################

missing_data_service_msg = "must select a data service first!"
missing_session_msg = "must start a session first!"


###############################################################################
# Class definitions                                                           #
###############################################################################

class PybackShell(cmd.Cmd):
    """CLI interface for pyback program"""

    intro = "Welcome to pyback! Enter your user ID to begin:"
    prompt = '(pyback) '

    def __init__(self):
        super(PybackShell, self).__init__()
        self.data_service = None
        self.session = None

    #
    # Control flow commands
    # # # # # # # # # # # #

    def do_quit(self, arg):
        '''exit program'''
        print("see ya, wouldn't want to be ya")
        if self.session:
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

    def do_select_data_service(self, config_filepath):
        '''select an existing data service'''
        try:
            self.data_service = select_data_service(config_filepath)
            print("selected data service!")
        except ValueError as err:
            print(err)

    def do_print_data_service(self, arg):
        '''print data service'''
        if self.data_service:
            print(self.data_service)
        else:
            print(missing_data_service_msg)

    #
    # Session starting commands
    # # # # # # # # # # # # # #

    def do_new_user_login(self, user_id):
        if self.data_service:
            new_user = SimpleUser(user_id)
            self.data_service.add_user(new_user)
            self.do_login(user_id)
        else:
            print(missing_data_service_msg)

    def do_login(self, user_id):
        if not user_id:
            print("Please specify a user ID")
            return

        if not self.data_service:
            print(missing_data_service_msg)

        if self.data_service.has_user(user_id):
            self.session = SimpleUserSession(self.data_service, user_id)
            self.prompt = '(pyback[{}]) '.format(user_id)
            print("logged in as {}!".format(user_id))
        else:
            print("User {} does not exist!".format(user_id))

    #
    # Session commands
    # # # # # # # # # # # #

    def do_add_data_location(self, args):
        if not self.session:
            print(missing_session_msg)
            return

        args = args.split(' ')

        if len(args) != 2:
            print("Please enter dir path and location name")
            return

        name = args[0]
        data_path = os.path.expanduser(args[1])

        data_location = SimpleDataLocation(id=name,
                                           name=name,
                                           path=data_path)

        try:
            self.session.add_data_location(data_location)
        except ValueError as err:
            print(err)

    def do_remove_data_location(self, data_location_id):
        if not self.session:
            print(missing_session_msg)
            return

        try:
            self.session.remove_data_location(data_location_id)
        except Exception:
            print("could not remove data location!")

    def do_add_save_location(self, args):
        if not self.session:
            print(missing_session_msg)
            return

        args = args.split(' ')
        if len(args) != 2:
            print("Enter save name and path")

        name = args[0]
        path = os.path.expanduser(args[1])

        save_location = LocalSaveLocation(id=name, save_path=path)
        self.session.add_save_location(save_location)

    def do_remove_save_location(self, save_location_id):
        if not self.session:
            print(missing_session_msg)
            return

        self.session.remove_save_location(save_location_id)

    def do_backup(self, arg):
        if not self.session:
            print(missing_session_msg)
            return

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
