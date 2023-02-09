from typing import Generic
from copy import deepcopy as dcp

from ..abs_paramters import S, T


class NaiveDict:
    def __init__(self, dct: dict = None):
        self.key_list = list()
        self.dict = dict()

        self._index = 0

        if dct is not None:
            for key in dct:
                self[key] = dct[key]

    def valid(self) -> bool:
        return len(self.key_list) == len(self.dict)

    def __setitem__(self, key, value):
        if key not in self.key_list:
            self.key_list.append(key)
        self.dict[key] = value
        assert self.valid()

    def __delitem__(self, key):
        if key in self.key_list:
            self.key_list.remove(key)
            self.dict.pop(key)
        assert self.valid()

    def __getitem__(self, key):
        return self.dict.get(key, None)

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        try:
            key = self.key_list[self._index]
            # value = self[key]
        except IndexError:
            self._index = 0
            raise StopIteration
        self._index += 1
        return key

    def __or__(self, other):
        ndict = dcp(self)
        for key in other:
            ndict[key] = other[key]
        return ndict

    def __ior__(self, other):
        for key in other:
            self[key] = other[key]
        return self

    def __len__(self):
        return len(self.key_list)

    def __str__(self):
        return f"{self.dict}"
