# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.distance._Chebyshev.

Chebyshev distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._Minkowski import Minkowski

__all__ = ['Chebyshev', 'chebyshev']


class Chebyshev(Minkowski):
    r"""Chebyshev distance.

    Euclidean distance is the chessboard distance,
    equivalent to Minkowski distance in :math:`L^\infty-space`.
    """

    def dist_abs(self, src, tar, qval=2, alphabet=None):
        r"""Return the Chebyshev distance between two strings.

        Args:
            src (str): Source string (or QGrams/Counter objects) for comparison
            tar (str): Target string (or QGrams/Counter objects) for comparison
            qval (int): The length of each q-gram; 0 for non-q-gram version
            alphabet (collection or int): The values or size of the alphabet

        Returns:
            float: The Chebyshev distance

        Examples:
            >>> cmp = Chebyshev()
            >>> cmp.dist_abs('cat', 'hat')
            1.0
            >>> cmp.dist_abs('Niall', 'Neil')
            1.0
            >>> cmp.dist_abs('Colin', 'Cuilen')
            1.0
            >>> cmp.dist_abs('ATCG', 'TAGC')
            1.0
            >>> cmp.dist_abs('ATCG', 'TAGC', qval=1)
            0.0
            >>> cmp.dist_abs('ATCGATTCGGAATTTC', 'TAGCATAATCGCCG', qval=1)
            3.0

        """
        return super(self.__class__, self).dist_abs(
            src, tar, qval, float('inf'), False, alphabet
        )

    def sim(self, *args, **kwargs):
        """Raise exception when called.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Raises:
            Exception: Method disabled for Chebyshev distance

        """
        raise Exception('Method disabled for Chebyshev distance.')

    def dist(self, *args, **kwargs):
        """Raise exception when called.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Raises:
            Exception: Method disabled for Chebyshev distance

        """
        raise Exception('Method disabled for Chebyshev distance.')


def chebyshev(src, tar, qval=2, alphabet=None):
    r"""Return the Chebyshev distance between two strings.

    This is a wrapper for the :py:meth:`Chebyshev.dist_abs`.

    Args:
        src (str): Source string (or QGrams/Counter objects) for comparison
        tar (str): Target string (or QGrams/Counter objects) for comparison
        qval (int): The length of each q-gram; 0 for non-q-gram version
        alphabet (collection or int): The values or size of the alphabet

    Returns:
        float: The Chebyshev distance

    Examples:
        >>> chebyshev('cat', 'hat')
        1.0
        >>> chebyshev('Niall', 'Neil')
        1.0
        >>> chebyshev('Colin', 'Cuilen')
        1.0
        >>> chebyshev('ATCG', 'TAGC')
        1.0
        >>> chebyshev('ATCG', 'TAGC', qval=1)
        0.0
        >>> chebyshev('ATCGATTCGGAATTTC', 'TAGCATAATCGCCG', qval=1)
        3.0

    """
    return Chebyshev().dist_abs(src, tar, qval, alphabet)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
