from copy import deepcopy as dcp


from .stat_dict import StatDict
from .int_list import IntList


class MatchDict(dict):
    def __init__(self, dct: dict = None):
        dict.__init__(self)
        if dct is not None:
            for key in dct:
                self[key] = dct[key]

    def to_stat_dict(self) -> StatDict:
        sdict = StatDict()
        for key in self:
            sdict[key] = self[key]
        return sdict

    @property
    def transpose(self):
        match_dict = self.__class__()
        for key in self:
            idx_list = self[key]
            for idx in idx_list:
                if idx not in match_dict:
                    match_dict[idx] = IntList()
                match_dict[idx].append(key)
        return match_dict

    @property
    def self_union(self) -> IntList:
        union_list = IntList()
        for i, key in enumerate(self):
            if i == 0:
                union_list = dcp(self[key])
            else:
                union_list += self[key]
        return union_list

    @property
    def self_intersection(self) -> IntList:
        intersection_list = IntList()
        for i, key in enumerate(self):
            if i == 0:
                intersection_list = dcp(self[key])
            else:
                intersection_list &= self[key]
        return intersection_list

    # @property
    # def self_complementary(self):
    #     """The complementary set of its union set"""
    #     complementary_list = IntList()
    #     return complementary_list

    def __setitem__(self, key, value):
        assert isinstance(key, int) and isinstance(value, (list, IntList))
        dict.__setitem__(self, key, IntList(value) if isinstance(value, list) else value)
