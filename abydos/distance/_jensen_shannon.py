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

"""abydos.distance._jensen_shannon.

Jensen-Shannon distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import log

from ._token_distance import _TokenDistance

__all__ = ['JensenShannon']


class JensenShannon(_TokenDistance):
    r"""Jensen-Shannon distance.

    Jensen-Shannon distance :cite:`Dagan:1999`

    .. versionadded:: 0.4.0
    """

    def __init__(self, **kwargs):
        """Initialize JensenShannon instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(JensenShannon, self).__init__(**kwargs)

    def dist_abs(self, src, tar):
        """Return the Jensen-Shannon distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Jensen-Shannon distance

        Examples
        --------
        >>> cmp = JensenShannon()
        >>> cmp.dist_abs('cat', 'hat')
        0.0
        >>> cmp.dist_abs('Niall', 'Neil')
        0.0
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        def entropy(prob):
            """Return the entropy of prob."""
            return -(prob * log(prob))

        src_total = sum(self._src_tokens.values())
        tar_total = sum(self._tar_tokens.values())

        diverg = 0.0
        for key in self._intersection().keys():
            p_src = self._src_tokens[key]/src_total
            p_tar = self._tar_tokens[key]/tar_total

            diverg -= entropy(p_src+p_tar)-entropy(p_src)-entropy(p_tar)

        return diverg

    def dist(self, src, tar):
        """Return the normalized Jensen-Shannon distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized Jensen-Shannon distance

        Examples
        --------
        >>> cmp = JensenShannon()
        >>> cmp.dist('cat', 'hat')
        0.0
        >>> cmp.dist('Niall', 'Neil')
        0.0
        >>> cmp.dist('aluminum', 'Catalan')
        0.0
        >>> cmp.dist('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return self.dist_abs(src, tar)/log(4)

if __name__ == '__main__':
    import doctest

    doctest.testmod()