
##############################################################################
# Imports                                                                    #
##############################################################################

import unittest
import sys

if 'D:\\Programs\\Cygwin\\home\\Brian\\pyback' not in sys.path:
    sys.path.append('D:\\Programs\\Cygwin\\home\\Brian\\pyback')

from client.user import User, SimpleUser


class SimpleUserTestCase(unittest.TestCase):

    def test_init(self):

        simple_user = SimpleUser(10)

        self.assertEqual(10, simple_user.get_id())


if __name__ == '__main__':
    unittest.main()
