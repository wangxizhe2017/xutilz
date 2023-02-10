from copy import deepcopy as dcp


class StatDict(dict):
    def __init__(self, dct: dict = None):
        dict.__init__(self)
        if dct is not None:
            for key in dct:
                self[key] = dct[key]

    def sort_by_key(self, reverse=False):
        return self.__class__(dct=dict(sorted(self.items(), reverse=reverse)))

    def __setitem__(self, key, value):
        assert isinstance(value, int)
        dict.__setitem__(self, key, value)

    def __add__(self, other):
        assert isinstance(other, self.__class__)
        sdict = dcp(self)
        for key in other:
            if key not in sdict:
                sdict[key] = 0
            sdict[key] += other[key]
        return sdict

    def __iadd__(self, other):
        assert isinstance(other, self.__class__)
        for key in other:
            if key not in self:
                self[key] = 0
            self[key] += other[key]
        return self

    def __sub__(self, other):
        assert isinstance(other, self.__class__)
        sdict = dcp(self)
        for key in other:
            if key not in sdict:
                sdict[key] = 0
            sdict[key] -= other[key]
        return sdict

    def __isub__(self, other):
        assert isinstance(other, self.__class__)
        for key in other:
            if key not in self:
                self[key] = 0
            self[key] -= other[key]
        return self
