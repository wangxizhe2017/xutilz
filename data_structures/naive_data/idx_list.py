from copy import deepcopy as dcp


class IdxList(list):
    def __init__(self, lst: list = None):
        list.__init__(self)
        if lst is not None:
            for value in lst:
                self.append(value)

    # overwrite
    def append(self, value: int) -> None:
        assert isinstance(value, int)
        if value not in self:
            list.append(self, value)

    # intersection
    def __and__(self, other):
        assert isinstance(other, self.__class__)
        i_list = self.__class__()
        for key in self:
            if key in other:
                i_list.append(key)
        return i_list

    # intersection
    def __iand__(self, other):
        assert isinstance(other, self.__class__)
        i_list = dcp(self)
        self.clear()
        for key in i_list:
            if key in other:
                self.append(key)
        return self

    # union
    def __add__(self, other):
        assert isinstance(other, self.__class__)
        i_list = dcp(self)
        for key in other:
            if key not in i_list:
                i_list.append(key)
        return i_list

    # union
    def __iadd__(self, other):
        assert isinstance(other, self.__class__)
        for key in other:
            if key not in self:
                self.append(key)
        return self

    # remove intersection
    def __sub__(self, other):
        assert isinstance(other, self.__class__)
        i_list = dcp(self)
        for key in other:
            if key in i_list:
                i_list.remove(key)
        return i_list

    # remove intersection
    def __isub__(self, other):
        assert isinstance(other, self.__class__)
        for key in other:
            if key in self:
                self.remove(key)
        return self

    # complementary set by a setup value
    def __rsub__(self, max_idx):
        """An integer subs a int_list"""
        assert isinstance(max_idx, int) and max(self) < max_idx
        complete_list = self.__class__(lst=list(range(max_idx)))
        return complete_list - self

    # complementary set by the max value of self
    def __neg__(self):
        max_idx = max(self)
        complete_list = self.__class__(lst=list(range(max_idx)))
        return complete_list - self

    @property
    def len(self) -> int:
        return len(self)
