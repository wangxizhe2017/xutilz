from typing import Callable

from .idx_list import IdxList
from .match_dict import MatchDict


match = lambda a, b: a == b
not_match = lambda a, b: a != b
abs_not_match = lambda a, b: a != b


class NaiveList(list):
    def __init__(self,
                 lst: list = None,
                 match_fn: Callable = None,
                 not_match_fn: Callable = None,
                 abs_not_match_fn: Callable = None):
        list.__init__(self)
        self._match_fn = match_fn
        self._not_match_fn = not_match_fn
        self._abs_not_match_fn = abs_not_match_fn

        if isinstance(lst, list):
            for item in lst:
                self.append(item)

    def set_match_fn(self, match_fn: Callable = match):
        self._match_fn = match_fn

    def set_not_match_fn(self, not_match_fn: Callable = not_match):
        self._not_match_fn = not_match_fn

    def set_abs_not_match_fn(self, abs_not_match_fn: Callable = abs_not_match):
        self._abs_not_match_fn = abs_not_match_fn

    def match(self, item_in) -> IdxList:
        assert isinstance(self._match_fn, Callable)
        m_idx_list = IdxList()
        for idx, item in enumerate(self):
            if self._match_fn(item, item_in):
                m_idx_list.append(idx)
        return m_idx_list

    # intersection match_dict of 2 naive_lists
    def __and__(self, other) -> MatchDict:
        assert isinstance(other, self.__class__)
        match_dict = MatchDict()
        for i, key in enumerate(other):
            pass
        return match_dict

    @property
    def len(self) -> int:
        return len(self)
