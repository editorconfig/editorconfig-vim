"""odict.py: An Ordered Dictionary object"""
# Copyright (C) 2005 Nicola Larosa, Michael Foord
# E-mail: nico AT tekNico DOT net, fuzzyman AT voidspace DOT org DOT uk
# Copyright (c) 2003-2010, Michael Foord
# E-mail : fuzzyman AT voidspace DOT org DOT uk
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#     * Neither the name of Michael Foord nor the name of Voidspace
#       may be used to endorse or promote products derived from this
#       software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from __future__ import generators
import sys
import warnings

from editorconfig.compat import slice


__docformat__ = "restructuredtext en"
__all__ = ['OrderedDict']


INTP_VER = sys.version_info[:2]
if INTP_VER < (2, 2):
    raise RuntimeError("Python v.2.2 or later required")


class OrderedDict(dict):
    """
    A class of dictionary that keeps the insertion order of keys.

    All appropriate methods return keys, items, or values in an ordered way.

    All normal dictionary methods are available. Update and comparison is
    restricted to other OrderedDict objects.

    Various sequence methods are available, including the ability to explicitly
    mutate the key ordering.

    __contains__ tests:

    >>> d = OrderedDict(((1, 3),))
    >>> 1 in d
    1
    >>> 4 in d
    0

    __getitem__ tests:

    >>> OrderedDict(((1, 3), (3, 2), (2, 1)))[2]
    1
    >>> OrderedDict(((1, 3), (3, 2), (2, 1)))[4]
    Traceback (most recent call last):
    KeyError: 4

    __len__ tests:

    >>> len(OrderedDict())
    0
    >>> len(OrderedDict(((1, 3), (3, 2), (2, 1))))
    3

    get tests:

    >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
    >>> d.get(1)
    3
    >>> d.get(4) is None
    1
    >>> d.get(4, 5)
    5
    >>> d
    OrderedDict([(1, 3), (3, 2), (2, 1)])

    has_key tests:

    >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
    >>> d.has_key(1)
    1
    >>> d.has_key(4)
    0
    """

    def __init__(self, init_val=(), strict=False):
        """
        Create a new ordered dictionary. Cannot init from a normal dict,
        nor from kwargs, since items order is undefined in those cases.

        If the ``strict`` keyword argument is ``True`` (``False`` is the
        default) then when doing slice assignment - the ``OrderedDict`` you are
        assigning from *must not* contain any keys in the remaining dict.

        >>> OrderedDict()
        OrderedDict([])
        >>> OrderedDict({1: 1})
        Traceback (most recent call last):
        TypeError: undefined order, cannot get items from dict
        >>> OrderedDict({1: 1}.items())
        OrderedDict([(1, 1)])
        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d
        OrderedDict([(1, 3), (3, 2), (2, 1)])
        >>> OrderedDict(d)
        OrderedDict([(1, 3), (3, 2), (2, 1)])
        """
        self.strict = strict
        dict.__init__(self)
        if isinstance(init_val, OrderedDict):
            self._sequence = init_val.keys()
            dict.update(self, init_val)
        elif isinstance(init_val, dict):
            # we lose compatibility with other ordered dict types this way
            raise TypeError('undefined order, cannot get items from dict')
        else:
            self._sequence = []
            self.update(init_val)

### Special methods ###

    def __delitem__(self, key):
        """
        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> del d[3]
        >>> d
        OrderedDict([(1, 3), (2, 1)])
        >>> del d[3]
        Traceback (most recent call last):
        KeyError: 3
        >>> d[3] = 2
        >>> d
        OrderedDict([(1, 3), (2, 1), (3, 2)])
        >>> del d[0:1]
        >>> d
        OrderedDict([(2, 1), (3, 2)])
        """
        if isinstance(key, slice):
            # FIXME: efficiency?
            keys = self._sequence[key]
            for entry in keys:
                dict.__delitem__(self, entry)
            del self._sequence[key]
        else:
            # do the dict.__delitem__ *first* as it raises
            # the more appropriate error
            dict.__delitem__(self, key)
            self._sequence.remove(key)

    def __eq__(self, other):
        """
        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d == OrderedDict(d)
        True
        >>> d == OrderedDict(((1, 3), (2, 1), (3, 2)))
        False
        >>> d == OrderedDict(((1, 0), (3, 2), (2, 1)))
        False
        >>> d == OrderedDict(((0, 3), (3, 2), (2, 1)))
        False
        >>> d == dict(d)
        False
        >>> d == False
        False
        """
        if isinstance(other, OrderedDict):
            # FIXME: efficiency?
            #   Generate both item lists for each compare
            return (self.items() == other.items())
        else:
            return False

    def __lt__(self, other):
        """
        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> c = OrderedDict(((0, 3), (3, 2), (2, 1)))
        >>> c < d
        True
        >>> d < c
        False
        >>> d < dict(c)
        Traceback (most recent call last):
        TypeError: Can only compare with other OrderedDicts
        """
        if not isinstance(other, OrderedDict):
            raise TypeError('Can only compare with other OrderedDicts')
        # FIXME: efficiency?
        #   Generate both item lists for each compare
        return (self.items() < other.items())

    def __le__(self, other):
        """
        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> c = OrderedDict(((0, 3), (3, 2), (2, 1)))
        >>> e = OrderedDict(d)
        >>> c <= d
        True
        >>> d <= c
        False
        >>> d <= dict(c)
        Traceback (most recent call last):
        TypeError: Can only compare with other OrderedDicts
        >>> d <= e
        True
        """
        if not isinstance(other, OrderedDict):
            raise TypeError('Can only compare with other OrderedDicts')
        # FIXME: efficiency?
        #   Generate both item lists for each compare
        return (self.items() <= other.items())

    def __ne__(self, other):
        """
        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d != OrderedDict(d)
        False
        >>> d != OrderedDict(((1, 3), (2, 1), (3, 2)))
        True
        >>> d != OrderedDict(((1, 0), (3, 2), (2, 1)))
        True
        >>> d == OrderedDict(((0, 3), (3, 2), (2, 1)))
        False
        >>> d != dict(d)
        True
        >>> d != False
        True
        """
        if isinstance(other, OrderedDict):
            # FIXME: efficiency?
            #   Generate both item lists for each compare
            return not (self.items() == other.items())
        else:
            return True

    def __gt__(self, other):
        """
        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> c = OrderedDict(((0, 3), (3, 2), (2, 1)))
        >>> d > c
        True
        >>> c > d
        False
        >>> d > dict(c)
        Traceback (most recent call last):
        TypeError: Can only compare with other OrderedDicts
        """
        if not isinstance(other, OrderedDict):
            raise TypeError('Can only compare with other OrderedDicts')
        # FIXME: efficiency?
        #   Generate both item lists for each compare
        return (self.items() > other.items())

    def __ge__(self, other):
        """
        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> c = OrderedDict(((0, 3), (3, 2), (2, 1)))
        >>> e = OrderedDict(d)
        >>> c >= d
        False
        >>> d >= c
        True
        >>> d >= dict(c)
        Traceback (most recent call last):
        TypeError: Can only compare with other OrderedDicts
        >>> e >= d
        True
        """
        if not isinstance(other, OrderedDict):
            raise TypeError('Can only compare with other OrderedDicts')
        # FIXME: efficiency?
        #   Generate both item lists for each compare
        return (self.items() >= other.items())

    def __repr__(self):
        """
        Used for __repr__ and __str__

        >>> r1 = repr(OrderedDict((('a', 'b'), ('c', 'd'), ('e', 'f'))))
        >>> r1
        "OrderedDict([('a', 'b'), ('c', 'd'), ('e', 'f')])"
        >>> r2 = repr(OrderedDict((('a', 'b'), ('e', 'f'), ('c', 'd'))))
        >>> r2
        "OrderedDict([('a', 'b'), ('e', 'f'), ('c', 'd')])"
        >>> r1 == str(OrderedDict((('a', 'b'), ('c', 'd'), ('e', 'f'))))
        True
        >>> r2 == str(OrderedDict((('a', 'b'), ('e', 'f'), ('c', 'd'))))
        True
        """
        return '%s([%s])' % (self.__class__.__name__, ', '.join(
            ['(%r, %r)' % (key, self[key]) for key in self._sequence]))

    def __setitem__(self, key, val):
        """
        Allows slice assignment, so long as the slice is an OrderedDict
        >>> d = OrderedDict()
        >>> d['a'] = 'b'
        >>> d['b'] = 'a'
        >>> d[3] = 12
        >>> d
        OrderedDict([('a', 'b'), ('b', 'a'), (3, 12)])
        >>> d[:] = OrderedDict(((1, 2), (2, 3), (3, 4)))
        >>> d
        OrderedDict([(1, 2), (2, 3), (3, 4)])
        >>> d[::2] = OrderedDict(((7, 8), (9, 10)))
        >>> d
        OrderedDict([(7, 8), (2, 3), (9, 10)])
        >>> d = OrderedDict(((0, 1), (1, 2), (2, 3), (3, 4)))
        >>> d[1:3] = OrderedDict(((1, 2), (5, 6), (7, 8)))
        >>> d
        OrderedDict([(0, 1), (1, 2), (5, 6), (7, 8), (3, 4)])
        >>> d = OrderedDict(((0, 1), (1, 2), (2, 3), (3, 4)), strict=True)
        >>> d[1:3] = OrderedDict(((1, 2), (5, 6), (7, 8)))
        >>> d
        OrderedDict([(0, 1), (1, 2), (5, 6), (7, 8), (3, 4)])

        >>> a = OrderedDict(((0, 1), (1, 2), (2, 3)), strict=True)
        >>> a[3] = 4
        >>> a
        OrderedDict([(0, 1), (1, 2), (2, 3), (3, 4)])
        >>> a[::1] = OrderedDict([(0, 1), (1, 2), (2, 3), (3, 4)])
        >>> a
        OrderedDict([(0, 1), (1, 2), (2, 3), (3, 4)])
        >>> a[:2] = OrderedDict([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
        Traceback (most recent call last):
        ValueError: slice assignment must be from unique keys
        >>> a = OrderedDict(((0, 1), (1, 2), (2, 3)))
        >>> a[3] = 4
        >>> a
        OrderedDict([(0, 1), (1, 2), (2, 3), (3, 4)])
        >>> a[::1] = OrderedDict([(0, 1), (1, 2), (2, 3), (3, 4)])
        >>> a
        OrderedDict([(0, 1), (1, 2), (2, 3), (3, 4)])
        >>> a[:2] = OrderedDict([(0, 1), (1, 2), (2, 3), (3, 4)])
        >>> a
        OrderedDict([(0, 1), (1, 2), (2, 3), (3, 4)])
        >>> a[::-1] = OrderedDict([(0, 1), (1, 2), (2, 3), (3, 4)])
        >>> a
        OrderedDict([(3, 4), (2, 3), (1, 2), (0, 1)])

        >>> d = OrderedDict([(0, 1), (1, 2), (2, 3), (3, 4)])
        >>> d[:1] = 3
        Traceback (most recent call last):
        TypeError: slice assignment requires an OrderedDict

        >>> d = OrderedDict([(0, 1), (1, 2), (2, 3), (3, 4)])
        >>> d[:1] = OrderedDict([(9, 8)])
        >>> d
        OrderedDict([(9, 8), (1, 2), (2, 3), (3, 4)])
        """
        if isinstance(key, slice):
            if not isinstance(val, OrderedDict):
                # FIXME: allow a list of tuples?
                raise TypeError('slice assignment requires an OrderedDict')
            keys = self._sequence[key]
            # NOTE: Could use ``range(*key.indices(len(self._sequence)))``
            indexes = range(len(self._sequence))[key]
            if key.step is None:
                # NOTE: new slice may not be the same size as the one being
                #   overwritten !
                # NOTE: What is the algorithm for an impossible slice?
                #   e.g. d[5:3]
                pos = key.start or 0
                del self[key]
                newkeys = val.keys()
                for k in newkeys:
                    if k in self:
                        if self.strict:
                            raise ValueError('slice assignment must be from '
                                'unique keys')
                        else:
                            # NOTE: This removes duplicate keys *first*
                            #   so start position might have changed?
                            del self[k]
                self._sequence = (self._sequence[:pos] + newkeys +
                    self._sequence[pos:])
                dict.update(self, val)
            else:
                # extended slice - length of new slice must be the same
                # as the one being replaced
                if len(keys) != len(val):
                    raise ValueError('attempt to assign sequence of size %s '
                        'to extended slice of size %s' % (len(val), len(keys)))
                # FIXME: efficiency?
                del self[key]
                item_list = zip(indexes, val.items())
                # smallest indexes first - higher indexes not guaranteed to
                # exist
                item_list.sort()
                for pos, (newkey, newval) in item_list:
                    if self.strict and newkey in self:
                        raise ValueError('slice assignment must be from unique'
                            ' keys')
                    self.insert(pos, newkey, newval)
        else:
            if key not in self:
                self._sequence.append(key)
            dict.__setitem__(self, key, val)

    def __getitem__(self, key):
        """
        Allows slicing. Returns an OrderedDict if you slice.
        >>> b = OrderedDict([(7, 0), (6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)])
        >>> b[::-1]
        OrderedDict([(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0)])
        >>> b[2:5]
        OrderedDict([(5, 2), (4, 3), (3, 4)])
        >>> type(b[2:4])
        <class '__main__.OrderedDict'>
        """
        if isinstance(key, slice):
            # FIXME: does this raise the error we want?
            keys = self._sequence[key]
            # FIXME: efficiency?
            return OrderedDict([(entry, self[entry]) for entry in keys])
        else:
            return dict.__getitem__(self, key)

    __str__ = __repr__

    def __setattr__(self, name, value):
        """
        Implemented so that accesses to ``sequence`` raise a warning and are
        diverted to the new ``setkeys`` method.
        """
        if name == 'sequence':
            warnings.warn('Use of the sequence attribute is deprecated.'
                ' Use the keys method instead.', DeprecationWarning)
            # NOTE: doesn't return anything
            self.setkeys(value)
        else:
            # FIXME: do we want to allow arbitrary setting of attributes?
            #   Or do we want to manage it?
            object.__setattr__(self, name, value)

    def __getattr__(self, name):
        """
        Implemented so that access to ``sequence`` raises a warning.

        >>> d = OrderedDict()
        >>> d.sequence
        []
        """
        if name == 'sequence':
            warnings.warn('Use of the sequence attribute is deprecated.'
                ' Use the keys method instead.', DeprecationWarning)
            # NOTE: Still (currently) returns a direct reference. Need to
            #   because code that uses sequence will expect to be able to
            #   mutate it in place.
            return self._sequence
        else:
            # raise the appropriate error
            raise AttributeError("OrderedDict has no '%s' attribute" % name)

    def __deepcopy__(self, memo):
        """
        To allow deepcopy to work with OrderedDict.

        >>> from copy import deepcopy
        >>> a = OrderedDict([(1, 1), (2, 2), (3, 3)])
        >>> a['test'] = {}
        >>> b = deepcopy(a)
        >>> b == a
        True
        >>> b is a
        False
        >>> a['test'] is b['test']
        False
        """
        from copy import deepcopy
        return self.__class__(deepcopy(self.items(), memo), self.strict)

### Read-only methods ###

    def copy(self):
        """
        >>> OrderedDict(((1, 3), (3, 2), (2, 1))).copy()
        OrderedDict([(1, 3), (3, 2), (2, 1)])
        """
        return OrderedDict(self)

    def items(self):
        """
        ``items`` returns a list of tuples representing all the
        ``(key, value)`` pairs in the dictionary.

        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d.items()
        [(1, 3), (3, 2), (2, 1)]
        >>> d.clear()
        >>> d.items()
        []
        """
        return zip(self._sequence, self.values())

    def keys(self):
        """
        Return a list of keys in the ``OrderedDict``.

        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d.keys()
        [1, 3, 2]
        """
        return self._sequence[:]

    def values(self, values=None):
        """
        Return a list of all the values in the OrderedDict.

        Optionally you can pass in a list of values, which will replace the
        current list. The value list must be the same len as the OrderedDict.

        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d.values()
        [3, 2, 1]
        """
        return [self[key] for key in self._sequence]

    def iteritems(self):
        """
        >>> ii = OrderedDict(((1, 3), (3, 2), (2, 1))).iteritems()
        >>> ii.next()
        (1, 3)
        >>> ii.next()
        (3, 2)
        >>> ii.next()
        (2, 1)
        >>> ii.next()
        Traceback (most recent call last):
        StopIteration
        """
        def make_iter(self=self):
            keys = self.iterkeys()
            while True:
                key = keys.next()
                yield (key, self[key])
        return make_iter()

    def iterkeys(self):
        """
        >>> ii = OrderedDict(((1, 3), (3, 2), (2, 1))).iterkeys()
        >>> ii.next()
        1
        >>> ii.next()
        3
        >>> ii.next()
        2
        >>> ii.next()
        Traceback (most recent call last):
        StopIteration
        """
        return iter(self._sequence)

    __iter__ = iterkeys

    def itervalues(self):
        """
        >>> iv = OrderedDict(((1, 3), (3, 2), (2, 1))).itervalues()
        >>> iv.next()
        3
        >>> iv.next()
        2
        >>> iv.next()
        1
        >>> iv.next()
        Traceback (most recent call last):
        StopIteration
        """
        def make_iter(self=self):
            keys = self.iterkeys()
            while True:
                yield self[keys.next()]
        return make_iter()

### Read-write methods ###

    def clear(self):
        """
        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d.clear()
        >>> d
        OrderedDict([])
        """
        dict.clear(self)
        self._sequence = []

    def pop(self, key, *args):
        """
        No dict.pop in Python 2.2, gotta reimplement it

        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d.pop(3)
        2
        >>> d
        OrderedDict([(1, 3), (2, 1)])
        >>> d.pop(4)
        Traceback (most recent call last):
        KeyError: 4
        >>> d.pop(4, 0)
        0
        >>> d.pop(4, 0, 1)
        Traceback (most recent call last):
        TypeError: pop expected at most 2 arguments, got 3
        """
        if len(args) > 1:
            raise TypeError('pop expected at most 2 arguments, got %s' %
                (len(args) + 1))
        if key in self:
            val = self[key]
            del self[key]
        else:
            try:
                val = args[0]
            except IndexError:
                raise KeyError(key)
        return val

    def popitem(self, i=-1):
        """
        Delete and return an item specified by index, not a random one as in
        dict. The index is -1 by default (the last item).

        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d.popitem()
        (2, 1)
        >>> d
        OrderedDict([(1, 3), (3, 2)])
        >>> d.popitem(0)
        (1, 3)
        >>> OrderedDict().popitem()
        Traceback (most recent call last):
        KeyError: 'popitem(): dictionary is empty'
        >>> d.popitem(2)
        Traceback (most recent call last):
        IndexError: popitem(): index 2 not valid
        """
        if not self._sequence:
            raise KeyError('popitem(): dictionary is empty')
        try:
            key = self._sequence[i]
        except IndexError:
            raise IndexError('popitem(): index %s not valid' % i)
        return (key, self.pop(key))

    def setdefault(self, key, defval=None):
        """
        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d.setdefault(1)
        3
        >>> d.setdefault(4) is None
        True
        >>> d
        OrderedDict([(1, 3), (3, 2), (2, 1), (4, None)])
        >>> d.setdefault(5, 0)
        0
        >>> d
        OrderedDict([(1, 3), (3, 2), (2, 1), (4, None), (5, 0)])
        """
        if key in self:
            return self[key]
        else:
            self[key] = defval
            return defval

    def update(self, from_od):
        """
        Update from another OrderedDict or sequence of (key, value) pairs

        >>> d = OrderedDict(((1, 0), (0, 1)))
        >>> d.update(OrderedDict(((1, 3), (3, 2), (2, 1))))
        >>> d
        OrderedDict([(1, 3), (0, 1), (3, 2), (2, 1)])
        >>> d.update({4: 4})
        Traceback (most recent call last):
        TypeError: undefined order, cannot get items from dict
        >>> d.update((4, 4))
        Traceback (most recent call last):
        TypeError: cannot convert dictionary update sequence element "4" to a 2-item sequence
        """
        if isinstance(from_od, OrderedDict):
            for key, val in from_od.items():
                self[key] = val
        elif isinstance(from_od, dict):
            # we lose compatibility with other ordered dict types this way
            raise TypeError('undefined order, cannot get items from dict')
        else:
            # FIXME: efficiency?
            # sequence of 2-item sequences, or error
            for item in from_od:
                try:
                    key, val = item
                except TypeError:
                    raise TypeError('cannot convert dictionary update'
                        ' sequence element "%s" to a 2-item sequence' % item)
                self[key] = val

    def rename(self, old_key, new_key):
        """
        Rename the key for a given value, without modifying sequence order.

        For the case where new_key already exists this raise an exception,
        since if new_key exists, it is ambiguous as to what happens to the
        associated values, and the position of new_key in the sequence.

        >>> od = OrderedDict()
        >>> od['a'] = 1
        >>> od['b'] = 2
        >>> od.items()
        [('a', 1), ('b', 2)]
        >>> od.rename('b', 'c')
        >>> od.items()
        [('a', 1), ('c', 2)]
        >>> od.rename('c', 'a')
        Traceback (most recent call last):
        ValueError: New key already exists: 'a'
        >>> od.rename('d', 'b')
        Traceback (most recent call last):
        KeyError: 'd'
        """
        if new_key == old_key:
            # no-op
            return
        if new_key in self:
            raise ValueError("New key already exists: %r" % new_key)
        # rename sequence entry
        value = self[old_key]
        old_idx = self._sequence.index(old_key)
        self._sequence[old_idx] = new_key
        # rename internal dict entry
        dict.__delitem__(self, old_key)
        dict.__setitem__(self, new_key, value)

    def setitems(self, items):
        """
        This method allows you to set the items in the dict.

        It takes a list of tuples - of the same sort returned by the ``items``
        method.

        >>> d = OrderedDict()
        >>> d.setitems(((3, 1), (2, 3), (1, 2)))
        >>> d
        OrderedDict([(3, 1), (2, 3), (1, 2)])
        """
        self.clear()
        # FIXME: this allows you to pass in an OrderedDict as well :-)
        self.update(items)

    def setkeys(self, keys):
        """
        ``setkeys`` all ows you to pass in a new list of keys which will
        replace the current set. This must contain the same set of keys, but
        need not be in the same order.

        If you pass in new keys that don't match, a ``KeyError`` will be
        raised.

        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d.keys()
        [1, 3, 2]
        >>> d.setkeys((1, 2, 3))
        >>> d
        OrderedDict([(1, 3), (2, 1), (3, 2)])
        >>> d.setkeys(['a', 'b', 'c'])
        Traceback (most recent call last):
        KeyError: 'Keylist is not the same as current keylist.'
        """
        # FIXME: Efficiency? (use set for Python 2.4 :-)
        # NOTE: list(keys) rather than keys[:] because keys[:] returns
        #   a tuple, if keys is a tuple.
        kcopy = list(keys)
        kcopy.sort()
        self._sequence.sort()
        if kcopy != self._sequence:
            raise KeyError('Keylist is not the same as current keylist.')
        # NOTE: This makes the _sequence attribute a new object, instead
        #       of changing it in place.
        # FIXME: efficiency?
        self._sequence = list(keys)

    def setvalues(self, values):
        """
        You can pass in a list of values, which will replace the
        current list. The value list must be the same len as the OrderedDict.

        (Or a ``ValueError`` is raised.)

        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d.setvalues((1, 2, 3))
        >>> d
        OrderedDict([(1, 1), (3, 2), (2, 3)])
        >>> d.setvalues([6])
        Traceback (most recent call last):
        ValueError: Value list is not the same length as the OrderedDict.
        """
        if len(values) != len(self):
            # FIXME: correct error to raise?
            raise ValueError('Value list is not the same length as the '
                'OrderedDict.')
        self.update(zip(self, values))

### Sequence Methods ###

    def index(self, key):
        """
        Return the position of the specified key in the OrderedDict.

        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d.index(3)
        1
        >>> d.index(4)
        Traceback (most recent call last):
        ValueError: 4 is not in list
        """
        return self._sequence.index(key)

    def insert(self, index, key, value):
        """
        Takes ``index``, ``key``, and ``value`` as arguments.

        Sets ``key`` to ``value``, so that ``key`` is at position ``index`` in
        the OrderedDict.

        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d.insert(0, 4, 0)
        >>> d
        OrderedDict([(4, 0), (1, 3), (3, 2), (2, 1)])
        >>> d.insert(0, 2, 1)
        >>> d
        OrderedDict([(2, 1), (4, 0), (1, 3), (3, 2)])
        >>> d.insert(8, 8, 1)
        >>> d
        OrderedDict([(2, 1), (4, 0), (1, 3), (3, 2), (8, 1)])
        """
        if key in self:
            # FIXME: efficiency?
            del self[key]
        self._sequence.insert(index, key)
        dict.__setitem__(self, key, value)

    def reverse(self):
        """
        Reverse the order of the OrderedDict.

        >>> d = OrderedDict(((1, 3), (3, 2), (2, 1)))
        >>> d.reverse()
        >>> d
        OrderedDict([(2, 1), (3, 2), (1, 3)])
        """
        self._sequence.reverse()

    def sort(self, *args, **kwargs):
        """
        Sort the key order in the OrderedDict.

        This method takes the same arguments as the ``list.sort`` method on
        your version of Python.

        >>> d = OrderedDict(((4, 1), (2, 2), (3, 3), (1, 4)))
        >>> d.sort()
        >>> d
        OrderedDict([(1, 4), (2, 2), (3, 3), (4, 1)])
        """
        self._sequence.sort(*args, **kwargs)


if __name__ == '__main__':
    # turn off warnings for tests
    warnings.filterwarnings('ignore')
    # run the code tests in doctest format
    import doctest
    m = sys.modules.get('__main__')
    globs = m.__dict__.copy()
    globs.update({
        'INTP_VER': INTP_VER,
    })
    doctest.testmod(m, globs=globs)
