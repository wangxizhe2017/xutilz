from typing import Callable

from ..naive_data import MatchDict, NaiveList


class SmartList(NaiveList):
    def __init__(self,
                 lst: list = None,
                 match_fn: Callable = None,
                 not_match_fn: Callable = None,
                 abs_not_match_fn: Callable = None):
        NaiveList.__init__(self, lst=lst, match_fn=match_fn, not_match_fn=not_match_fn, abs_not_match_fn=abs_not_match_fn)

    def match(self, item_in) -> list:
        match_list = list()
        for idx, item in enumerate(self):
            if self._match_fn(item, item_in):
                match_list.append(idx)
        return match_list


