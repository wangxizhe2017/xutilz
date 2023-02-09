from typing import Callable


match = lambda a, b: a == b
not_match = lambda a, b: a != b
abs_not_match = lambda a, b: a != b


class NaiveList(list):
    def __init__(self,
                 lst: list = None,
                 match_fn: Callable = match,
                 not_match_fn: Callable = not_match,
                 abs_not_match_fn: Callable = abs_not_match):
        list.__init__(self)
        self._match_fn = match_fn
        self._not_match_fn = not_match_fn
        self._abs_not_match_fn = abs_not_match_fn

        if isinstance(lst, list):
            for item in lst:
                self.append(item)

    def set_match_fn(self, match_fn: Callable = None):
        self._match_fn = match_fn

    def set_not_match_fn(self, not_match_fn: Callable = None):
        self._not_match_fn = not_match_fn

    def set_abs_not_match_fn(self, abs_not_match_fn: Callable = None):
        self._abs_not_match_fn = abs_not_match_fn

    @property
    def len(self) -> int:
        return len(self)
