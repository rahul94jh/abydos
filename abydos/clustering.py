# -*- coding: utf-8 -*-
"""abydos.clustering

The clustering module implements clustering algorithms such as string
fingerprinting, k-nearest neighbors, and ...


Copyright 2014-2015 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""


from __future__ import unicode_literals
from __future__ import division
import unicodedata
from itertools import groupby
from ._compat import _unicode, _range
from .phonetic import double_metaphone
from .qgram import QGrams
from .distance import sim
import abydos.stats as stats

def fingerprint(phrase):
    """Return the fingerprint of a phrase

    Arguments:
    phrase -- a string to calculate the fingerprint of

    Description:
    The fingerprint of a string is a string consisting of all of the unique
    words in a string, alphabetized & concatenated with intervening spaces
    """
    phrase = unicodedata.normalize('NFKD', _unicode(phrase.strip().lower()))
    phrase = ''.join([c for c in phrase if c.isalnum() or c.isspace()])
    phrase = ' '.join(sorted(list(set(phrase.split()))))
    return phrase


def qgram_fingerprint(phrase, qval=2, start_stop=''):
    """Return the q-gram fingerprint of a phrase

    Arguments:
    phrase -- a string to calculate the q-gram fingerprint of
    qval -- the length of each q-gram (by default 2)
    start_stop -- the start & stop symbol(s) to concatenate on either end of
        the phrase, as defined in abydos.util.qgram()

    Description:
    A q-gram fingerprint is a string consisting of all of the unique q-grams
    in a string, alphabetized & concatenated.
    """
    phrase = unicodedata.normalize('NFKD', _unicode(phrase.strip().lower()))
    phrase = ''.join([c for c in phrase if c.isalnum()])
    phrase = QGrams(phrase, qval, start_stop)
    phrase = ''.join(sorted(list(phrase)))
    return phrase


def phonetic_fingerprint(phrase, phonetic_algorithm=double_metaphone, *args):
    """Return the phonetic fingerprint of a phrase

    Arguments:
    phrase -- a string to calculate the phonetic fingerprint of
    phonetic_algorithm -- a phonetic algorithm that takes a string and returns
        a string (presumably a phonetic representation of the original string)
        By default, this function uses double_metaphone() from abydos.phonetic.
    *args -- additional arguments to pass to the phonetic algorithm, along with
        the phrase itself

    Description:
    A phonetic fingerprint is identical to a standard string fingerprint, as
    implemented in abydos.clustering.fingerprint(), but performs the
    fingerprinting function after converting the string to its phonetic form,
    as determined by some phonetic algorithm.
    """
    phonetic = ''
    for word in phrase.split():
        word = phonetic_algorithm(word, *args)
        if not isinstance(word, _unicode) and hasattr(word, '__iter__'):
            word = word[0]
        phonetic += word + ' '
    phonetic = phonetic[:-1]
    return fingerprint(phonetic)


def skeleton_key(word):
    """Return the skeleton key of a word

    Arguments:
    word -- the word to transform into its skeleton key

    Description:
    The skeleton key of a word is defined in:
    Pollock, Joseph J. and Antonio Zamora. 1984. "Automatic Spelling Correction
    in Scientific and Scholarly Text." Communications of the ACM, 27(4).
    358--368. <http://dl.acm.org/citation.cfm?id=358048>
    """
    _vowels = 'AEIOU'

    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = ''.join([c for c in word if c in
                    tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

    start = word[0:1]
    consonant_part = ''
    vowel_part = ''

    # add consonants & vowels to to separate strings
    # (omitting the first char & duplicates)
    for char in word[1:]:
        if char != start:
            if char in _vowels:
                if char not in vowel_part:
                    vowel_part += char
            elif char not in consonant_part:
                consonant_part += char
    # return the first char followed by consonants followed by vowels
    return start + consonant_part + vowel_part


def omission_key(word):
    """Return the omission key of a word

    Arguments:
    word -- the word to transform into its omission key

    Description:
    The omission key of a word is defined in:
    Pollock, Joseph J. and Antonio Zamora. 1984. "Automatic Spelling Correction
    in Scientific and Scholarly Text." Communications of the ACM, 27(4).
    358--368. <http://dl.acm.org/citation.cfm?id=358048>
    """
    _consonants = 'JKQXZVWYBFMGPDHCLNTSR'

    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = ''.join([c for c in word if c in
                    tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

    key = ''

    # add consonants in order supplied by _consonants (no duplicates)
    for char in _consonants:
        if char in word:
            key += char

    # add vowels in order they appeared in the word (no duplicates)
    for char in word:
        if char not in _consonants and char not in key:
            key += char

    return key


def bwt(word, terminator='\0'):
    """Return the Burrows-Wheeler transformed form of a word

    Arguments:
    word -- the word to transform using BWT
    terminator -- a character to add to word to signal the end of the string

    Description:
    The Burrows-Wheeler transform is an attempt at placing similar characters
    together to improve compression.
    Cf. https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform
    """
    if word:
        assert terminator not in word, ('Specified terminator, '+
                                        (terminator if terminator else '\\0')+
                                        ', already in word.')
        word += terminator
        wordlist = sorted([word[i:]+word[:i] for i in _range(len(word))])
        return ''.join([w[-1] for w in wordlist])
    return terminator


def bwt_decode(code, terminator='\0'):
    """Return a word decoded from BWT form

    Arguments:
    code -- the word to transform from BWT form
    terminator -- a character added to word to signal the end of the string

    Description:
    The Burrows-Wheeler transform is an attempt at placing similar characters
    together to improve compression. This function reverses the transform.
    Cf. https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform
    """
    if code:
        assert terminator in code, ('Specified terminator, '+
                                    (terminator if terminator else '\\0')+
                                    ', absent from word.')
        wordlist = [''] * len(code)
        for i in _range(len(code)):
            wordlist = sorted([code[i]+wordlist[i] for i in _range(len(code))])
        s = [w for w in wordlist if w[-1] == terminator][0]
        return s.rstrip(terminator)
    return ''


def rle_encode(text, use_bwt=True):
    """Simple, crude run-length-encoding (RLE) encoder
    http://rosettacode.org/wiki/Run-length_encoding#Python

    Arguments:
    text -- a text string to encode
    use_bwt -- boolean indicating whether to perform BWT encoding before RLE

    Description:
    Based on http://rosettacode.org/wiki/Run-length_encoding#Python

    Digits 0-9 cannot be in text.
    """
    if use_bwt:
        text = bwt(text)
    text = [(len(list(g)),k) for k,g in groupby(text)]
    text = [(str(n)+k if n>2 else (k if n==1 else 2*k)) for n,k in text]
    return ''.join(text)

def rle_decode(text, use_bwt=True):
    """Simple, crude run-length-encoding (RLE) decoder

    Arguments:
    text -- a text string to decode
    use_bwt -- boolean indicating whether to perform BWT decoding after RLE
        decoding

    Description:
    Based on http://rosettacode.org/wiki/Run-length_encoding#Python

    Digits 0-9 cannot have been in the original text.
    """
    mult = ''
    decoded = []
    for l in list(text):
        if not l.isdigit():
            if mult:
                decoded.append(int(mult)*l)
                mult = ''
            else:
                decoded.append(l)
        else:
            mult += l

    text = ''.join(decoded)
    if use_bwt:
        text = bwt_decode(text)
    return text


def mean_pairwise_similarity(collection, metric=sim,
                             meanfunc=stats.hmean, symmetric=False):
    """Return the mean pairwise similarity of a collection of strings

    Arguments:
    collection -- a tuple, list, or set of terms or a string that can be split
    metric -- a similarity metric function
    mean -- a mean function that takes a list of values and returns a float
    symmetric -- set to True if all pairwise similarities should be calculated
                    in both directions
    """
    if hasattr(collection, 'split'):
        collection = collection.split()
    if not hasattr(collection, '__iter__'):
        raise ValueError('collection is neither a string nor iterable type')
    elif len(collection) < 2:
        raise ValueError('collection has fewer than two members')

    pairwise_values = []

    for i, word1 in list(enumerate(collection)):
        for j, word2 in list(enumerate(collection)):
            if i != j:
                pairwise_values.append(metric(word1, word2))
                if symmetric:
                    pairwise_values.append(metric(word2, word1))

    if not hasattr(meanfunc, '__call__'):
        raise ValueError('meanfunc must be a function')
    return meanfunc(pairwise_values)
