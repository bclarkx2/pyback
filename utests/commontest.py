
##############################################################################
# Imports                                                                    #
##############################################################################

from unittest.mock import patch, MagicMock


##############################################################################
# Helper Classes                                                             #
##############################################################################

class MultiPatch(object):
    """allows patching many objects at once"""

    def __init__(self, patches):

        self.patchers = []

        for patchable in patches:

            try:
                self.patchers.append(patch(patchable[0], patchable[1]))
            except IndexError:
                self.patchers.append(patch(patchable[0], MagicMock()))

    def __enter__(self):
        for patcher in self.patchers:
            patcher.start()

    def __exit__(self, *args):
        for patcher in self.patchers:
            patcher.stop()
