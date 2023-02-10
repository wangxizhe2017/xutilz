from copy import deepcopy as dcp


from .stat_dict import StatDict
from .idx_list import IdxList


class MatchDict(dict):
    def __init__(self, dct: dict = None):
        dict.__init__(self)
        if dct is not None:
            for key in dct:
                self[key] = dct[key]

    def sort_by_key(self, reverse=False):
        return self.__class__(dct=dict(sorted(self.items(), reverse=reverse)))

    def to_stat_dict(self) -> StatDict:
        sdict = StatDict()
        for key in self:
            sdict[key] = len(self[key])
        return sdict

    @property
    def transpose(self):
        match_dict = self.__class__()
        for key in self:
            idx_list = self[key]
            for idx in idx_list:
                if idx not in match_dict:
                    match_dict[idx] = IdxList()
                match_dict[idx].append(key)
        return match_dict

    @property
    def self_union(self) -> IdxList:
        union_list = IdxList()
        for i, key in enumerate(self):
            if i == 0:
                union_list = dcp(self[key])
            else:
                union_list += self[key]
        return union_list

    @property
    def self_intersection(self) -> IdxList:
        intersection_list = IdxList()
        for i, key in enumerate(self):
            if i == 0:
                intersection_list = dcp(self[key])
            else:
                intersection_list &= self[key]
        return intersection_list

    # @property
    # def self_complementary(self):
    #     """The complementary set of its union set"""
    #     complementary_list = IdxList()
    #     return complementary_list

    def __setitem__(self, key, value):
        assert isinstance(key, int) and isinstance(value, (IdxList, list))
        dict.__setitem__(self, key, value if isinstance(value, IdxList) else IdxList(value))

    # intersection of 2 match_dicts
    def __and__(self, other):
        assert isinstance(other, self.__class__)
        m_dict = dcp(self)
        for key in other:
            if key not in m_dict:
                m_dict[key] = dcp(other[key])
            else:
                m_dict[key] &= other[key]
        return m_dict

    # intersection of 2 match_dicts
    def __iand__(self, other):
        assert isinstance(other, self.__class__)
        for key in other:
            if key not in self:
                self[key] = dcp(other[key])
            else:
                self[key] &= other[key]
        return self

    # union of 2 match_dicts
    def __add__(self, other):
        assert isinstance(other, self.__class__)
        m_dict = dcp(self)
        for key in other:
            if key not in m_dict:
                m_dict[key] = dcp(other[key])
            else:
                m_dict[key] += other[key]
        return m_dict

    # union of 2 match_dicts
    def __iadd__(self, other):
        assert isinstance(other, self.__class__)
        for key in other:
            if key not in self:
                self[key] = dcp(other[key])
            else:
                self[key] += other[key]
        return self

    # remove intersection
    def __sub__(self, other):
        assert isinstance(other, self.__class__)
        m_dict = dcp(self)
        for key in other:
            if key not in m_dict:
                m_dict[key] = dcp(other[key])
            else:
                m_dict[key] -= other[key]
        return m_dict

    # remove intersection
    def __isub__(self, other):
        assert isinstance(other, self.__class__)
        for key in other:
            if key not in self:
                self[key] = dcp(other[key])
            else:
                self[key] -= other[key]
        return self
