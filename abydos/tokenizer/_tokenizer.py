# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.tokenizer._tokenize.

_Tokenizer base class
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import Counter

__all__ = ['_Tokenizer']


class _Tokenizer(object):
    """Abstract _Tokenizer class.

    .. versionadded:: 0.4.0
    """

    def __init__(self, scaler=None, *args, **kwargs):
        """Initialize Tokenizer.

        Parameters
        ----------
        scaler : None, str, or function
            A scaling function for the Counter:

                - None : no scaling
                - 'set' : All non-zero values are set to 1.
                - a callable function : The function is applied to each value
                  in the Counter. Some useful functions include math.exp,
                  math.log1p, math.sqrt, and indexes into interesting integer
                  sequences such as the Fibonacci sequence.


        .. versionadded:: 0.4.0

        """
        super(_Tokenizer, self).__init__()

        self.scaler = scaler
        self._tokens = Counter()
        self._string = ''
        self._ordered_list = []

    def tokenize(self, string=None):
        """Tokenize the term and store it.

        The tokenized term is stored as an ordered list and as a Counter
        object.

        Parameters
        ----------
        string : str
            The string to tokenize


        .. versionadded:: 0.4.0

        """
        if string is not None:
            self._string = string
            self._ordered_list = [self._string]

        self._tokens = Counter(self._ordered_list)
        return self

    def count(self):
        """Return token count.

        Returns
        -------
        int
            The total count of tokens

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.count()
        1


        .. versionadded:: 0.4.0

        """
        return sum(self.get_counter().values())

    def count_unique(self):
        """Return the number of unique elements.

        Returns
        -------
        int
            The number of unique tokens

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.count_unique()
        1


        .. versionadded:: 0.4.0

        """
        return len(self._tokens.values())

    def get_counter(self):
        """Return the tokens as a Counter object.

        Returns
        -------
        Counter
            The Counter of tokens

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.get_counter()
        Counter({'term': 1})


        .. versionadded:: 0.4.0

        """
        if self.scaler is None:
            return self._tokens
        elif self.scaler == 'set':
            return Counter({key: 1 for key in self._tokens.keys()})
        elif callable(self.scaler):
            return Counter(
                {key: self.scaler(val) for key, val in self._tokens.items()}
            )
        raise ValueError('Unsupported scaler value.')

    def get_set(self):
        """Return the unique tokens as a set.

        Returns
        -------
        Counter
            The set of tokens

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.get_set()
        {'term'}


        .. versionadded:: 0.4.0

        """
        return set(self._tokens.keys())

    def get_list(self):
        """Return the tokens as an ordered list.

        Returns
        -------
        Counter
            The list of q-grams in the order they were added.

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.get_list()
        ['term']


        .. versionadded:: 0.4.0

        """
        return self._ordered_list


if __name__ == '__main__':
    import doctest

    doctest.testmod()
