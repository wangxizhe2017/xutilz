from pathlib import Path
from abc import abstractmethod

from xfile import load_json, get_dir_list_in_dir


class TraverseBase:
    def __init__(self, wrapper, *args, **kwargs):
        self.wrapper = wrapper

    @abstractmethod
    def run_wrapper(self, top_caller, caller, *args, **kwargs):
        pass

    def __call__(self, top_caller, caller, *args, **kwargs):
        return self.run_wrapper(top_caller=top_caller, caller=caller, *args, **kwargs)

    def __get__(self, top_caller, top_caller_type):
        def wrap(*args, **kwargs):
            return self.run_wrapper(top_caller=top_caller, caller=self, *args, **kwargs)
        return wrap


class TraversePath(TraverseBase):
    """wrapper interface: fn(self, path, **kwargs)"""
    def __init__(self, wrapper, *args, **kwargs):
        super().__init__(wrapper, *args, **kwargs)
        self.path = kwargs.get("path", None)
        self.sub_dir = kwargs.get("sub_dir", None)
        self.get_path_list_fn = kwargs.get("get_path_list_fn", None)

    def run_wrapper(self, top_caller, caller, *args, **kwargs):
        res_list = []
        # dynamic "path"
        p = self.path if self.path is not None else kwargs.pop("path", None)
        assert p is not None
        path = p if isinstance(p, Path) else Path(p)
        # dynamic "sub_dir"
        sub_dir = self.sub_dir if self.sub_dir is not None else kwargs.pop("sub_dir", None)
        # dynamic "get_path_list_fn"
        get_path_list_fn = self.get_path_list_fn if self.get_path_list_fn is not None else \
            kwargs.pop("get_path_list_fn", get_dir_list_in_dir)

        if isinstance(self.wrapper, self.__class__.__base__):
            # in this branch, self.wrapper is a sub decorator object
            sub_path_list = get_path_list_fn(path)
            for sub_path in sub_path_list:
                target_path = sub_path / sub_dir if sub_dir is not None else sub_path
                res = self.wrapper(top_caller=top_caller, caller=self, path=target_path, **kwargs)
                res_list.append(res)
        else:
            # in this branch, self.wrapper is the actual function called in the executing object
            sub_path_list = get_path_list_fn(path)
            for sub_path in sub_path_list:
                target_path = sub_path / sub_dir if sub_dir is not None else sub_path
                res = self.wrapper(self=top_caller, path=target_path, **kwargs)
                res_list.append(res)

        return res_list


class TraverseJSON(TraverseBase):
    """wrapper interface: fn(self, key, jn, **kwargs)"""
    def __init__(self, wrapper, *args, **kwargs):
        super().__init__(wrapper, *args, **kwargs)
        p = kwargs.get("path", None)
        self.path = p if isinstance(p, Path) else Path(p) if p is not None else None

    def run_wrapper(self, top_caller, caller, *args, **kwargs):
        res_list = []
        p = self.path if self.path is not None else kwargs.pop("path", None)
        path = p if isinstance(p, Path) else Path(p) if p is not None else None
        annotation_json = load_json(path) if path is not None else None
        jn = kwargs.pop("jn", annotation_json)

        if isinstance(self.wrapper, self.__class__.__base__):
            # in this branch, self.wrapper is a sub decorator object
            if isinstance(jn, dict):
                for key in jn:
                    res = self.wrapper(top_caller=top_caller, caller=self, jn=jn[key], **kwargs)
                    res_list.append(res)
            elif isinstance(jn, list):
                for element in jn:
                    res = self.wrapper(top_caller=top_caller, caller=self, jn=element, **kwargs)
                    res_list.append(res)
            elif isinstance(jn, str) or isinstance(jn, int) or isinstance(jn, float) or \
                 isinstance(jn, bool) or isinstance(jn, complex) or isinstance(jn, tuple):
                res = self.wrapper(top_caller=top_caller, caller=self, jn=jn, **kwargs)
                res_list.append(res)
            else:
                print(f"{jn} is unknown data type")
        else:
            # in this branch, self.wrapper is the actual function called in the executing object
            if isinstance(jn, dict):
                for key in jn:
                    res = self.wrapper(self=top_caller, key=key, jn=jn[key], **kwargs)
                    res_list.append(res)
            elif isinstance(jn, list):
                for i, element in enumerate(jn):
                    res = self.wrapper(self=top_caller, key=i, jn=element, **kwargs)
                    res_list.append(res)
            elif isinstance(jn, str) or isinstance(jn, int) or isinstance(jn, float) or \
                 isinstance(jn, bool) or isinstance(jn, complex) or isinstance(jn, tuple):
                res = self.wrapper(self=top_caller, key=None, jn=jn, **kwargs)
                res_list.append(res)
            else:
                print(f"{jn} is unknown data type")

        return res_list

