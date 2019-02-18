# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""abydos.tests.distance.test_distance_iterative_substring.

This module contains unit tests for abydos.distance.IterativeSubString
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import IterativeSubString


class IterativeSubStringTestCases(unittest.TestCase):
    """Test IterativeSubString functions.

    abydos.distance.IterativeSubString
    """

    cmp = IterativeSubString()

    def test_iterative_substring_sim(self):
        """Test abydos.distance.IterativeSubString.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.1)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.1)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.1)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.1)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6618421053
        )


if __name__ == '__main__':
    unittest.main()