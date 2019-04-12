# -*- coding: utf-8 -*-

# Copyright 2018-2019 by Christopher C. Little.
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

"""abydos.tokenizer._nltk.

NLTK tokenizer wrapper class
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._tokenizer import _Tokenizer


class NLTKTokenizer(_Tokenizer):
    """NLTK tokenizer wrapper class.

    .. versionadded:: 0.4.0
    """

    def __init__(self, nltk_tokenizer=None, scaler=None):
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
        nltk_tokenizer : Object
            An instantiated tokenizer from NLTK.


        .. versionadded:: 0.4.0

        """
        super(NLTKTokenizer, self).__init__(scaler)

        if 'nltk.tokenize' in str(type(nltk_tokenizer)) and hasattr(
            nltk_tokenizer, 'tokenize'
        ):
            self.nltk_tokenizer = nltk_tokenizer
        else:
            raise TypeError(
                'nltk_tokenizer must be an initialized tokenizer from the'
                + ' NLTK package (e.g. TweetTokenizer()).'
            )

    def tokenize(self, string):
        """Tokenize the term and store it.

        The tokenized term is stored as an ordered list and as a Counter
        object.

        Parameters
        ----------
        string : str
            The string to tokenize

        Examples
        --------
        >>> from nltk.tokenize.casual import TweetTokenizer
        >>> nltk_tok = TweetTokenizer()
        >>> NLTKTokenizer(nltk_tokenizer=nltk_tok).\
tokenize('.@Twitter Today is #lit!')
        NLTKTokenizer({'.': 1, '@Twitter': 1, 'Today': 1, 'is': 1, '#lit': 1, \
'!': 1})

        .. versionadded:: 0.4.0

        """
        self._string = string
        self._ordered_tokens = self.nltk_tokenizer.tokenize(string)
        super(NLTKTokenizer, self).tokenize()
        return self


if __name__ == '__main__':
    import doctest

    doctest.testmod()
