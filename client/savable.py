
##############################################################################
# Imports                                                                    #
##############################################################################

import json


##############################################################################
# Base class                                                                 #
##############################################################################

class Savable(object):
    """Implement Savable to ensure an object can be JSON saved

    Classes extending Savable must return a JSON Encoder and Decoder. This
    will allow a user of the extended class to use json.dump or json.dumps
    to serialize the class into JSON. Thus, it could be saved.
    """

    def encoder(self):
        raise NotImplementedError("Implement Me!")

    def decoder(self):
        raise NotImplementedError("Implement Me!")


class DefaultSavable(Savable):
    """Default implementation of Savable

    Extend DefaultSavable to make a class Savable without having to define a custom
    JSON encoder. It will just return the default json encoder/decoder
    """

    def encoder(self):
        return json.JSONEncoder

    def decoder(self):
        return json.JSONDecoder
