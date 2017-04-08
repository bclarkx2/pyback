
##############################################################################
# Imports                                                                    #
##############################################################################

import json


##############################################################################
# Base class                                                                 #
##############################################################################

class Savable(object):  # pragma: no cover
    """Implement Savable to ensure an object can be JSON saved

    Classes extending Savable must return a JSON Encoder and Decoder. This
    will allow a user of the extended class to use json.dump or json.dumps
    to serialize the class into JSON. Thus, it could be saved.
    """

    def encoder(self):
        raise NotImplementedError("Implement Me!")

    def decoder(self):
        raise NotImplementedError("Implement Me!")


##############################################################################
# Implementations                                                            #
##############################################################################

class DefaultSavable(Savable):  # pragma: no cover
    """Default implementation of Savable

    Extend DefaultSavable to make a class Savable without having to define a
    custom JSON encoder. It will just return the default json encoder/decoder
    """

    def encoder(self):
        return json.JSONEncoder

    def decoder(self):
        return json.JSONDecoder


class CustomSavable(Savable):

    def to_dict(self):  # pragma: no cover
        raise NotImplementedError("Implement me or else!")

    def make_from_dict(self, input_dict):  # pragma: no cover
        raise NotImplementedError("Implement me or else!")

    def validate_dict(self, input_dict):  # pragma: no cover
        raise NotImplementedError("Implement me or else!")

    def encoder(self):
        return self.build_custom_encoder()

    def decoder(self):
        return self.build_custom_decoder()

    def build_custom_encoder(self):
        """factory method to build a custom encoder

        Uses closure to create encoder using methods that all
        Savable objects must have
        """

        current_class = self.__class__
        to_dict = self.to_dict

        class CustomEncoder(json.JSONEncoder):

            def default(self, o):

                if isinstance(o, current_class):
                    return to_dict()
                else:
                    return json.JSONEncoder.default(self, o)

        return CustomEncoder

    def build_custom_decoder(self):
        """factory method to build a custom decoder

        Uses closure to create decoder using methods that all
        Savable objects must have
        """

        validator = self.validate_dict
        object_builder = self.make_from_dict

        class CustomDecoder(json.JSONDecoder):

            def __init__(self):
                json.JSONDecoder.__init__(self, object_hook=self.decode)

            def decode(self, incoming_str):

                incoming_dict = json.loads(incoming_str)

                is_valid_dict = validator(incoming_dict)

                if is_valid_dict:
                    return object_builder(incoming_dict)
                else:
                    return incoming_dict

        return CustomDecoder
