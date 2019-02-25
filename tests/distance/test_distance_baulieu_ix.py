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

"""abydos.tests.distance.test_distance_baulieu_ix.

This module contains unit tests for abydos.distance.BaulieuIX
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import BaulieuIX


class BaulieuIXTestCases(unittest.TestCase):
    """Test BaulieuIX functions.

    abydos.distance.BaulieuIX
    """

    cmp = BaulieuIX()
    cmp_no_d = BaulieuIX(alphabet=1)

    def test_baulieu_ix_dist(self):
        """Test abydos.distance.BaulieuIX.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.002551020408163265)
        self.assertEqual(self.cmp.dist('', 'a'), 0.005089058524173028)
        self.assertEqual(self.cmp.dist('abc', ''), 0.00510204081632653)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.01015228426395939)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.019011406844106463)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0114358323)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0114358323)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0114358323)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0114358323)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0127064803
        )

    def test_baulieu_ix_sim(self):
        """Test abydos.distance.BaulieuIX.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.9974489795918368)
        self.assertEqual(self.cmp.sim('', 'a'), 0.9949109414758269)
        self.assertEqual(self.cmp.sim('abc', ''), 0.9948979591836735)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.9898477157360406)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.9809885931558935)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9885641677)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9885641677)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9885641677)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9885641677)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9872935197
        )


if __name__ == '__main__':
    unittest.main()