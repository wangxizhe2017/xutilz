import os
import json
import yaml
import datetime
import glob
from os import listdir
from pathlib import Path
from os.path import isfile

from functools import wraps
from shutil import copyfile, copytree
from typing import Any, Union, Callable
from multipledispatch import dispatch

from ximage import images_identical


def ensure_path(path: Union[Path, str]):
    """
    :param path: can be both a dir or a file
    """
    p = path if isinstance(path, Path) else Path(path)
    p.mkdir(parents=True, exist_ok=True)


def path_exists(path: Union[Path, str]) -> bool:
    """
    :param path: can be both a dir or a file
    :return: bool
    """
    p = path if isinstance(path, Path) else Path(path)
    return p.exists()


def load_text(path: Union[Path, str]) -> str:
    """
    :param path: can be both a dir or a file
    :return: str: the loaded context
    """
    assert path_exists(path), "{} not exists.".format(path)

    with open(path, "r") as f:
        txt_str = f.read()
        f.close()

        if txt_str[-1] == "\n":
            return txt_str[:-1]

        return txt_str


def load_xml(path: Union[Path, str]):
    pass


def load_json(path: Union[Path, str]):
    """
    :param path: can be both a dir or a file
    :return: dict: the loaded json
    """
    assert path_exists(path)

    with open(path) as f:
        return json.load(f)


def load_yaml(path: Union[Path, str]):
    """
    :param path: can be both a dir or a file
    :return: Union[dict, list, None]: the loaded yaml
    """
    assert path_exists(path)

    with open(path, "r") as stream:
        return yaml.safe_load(stream)


def get_dir_list_in_dir(path: Union[Path, str], include_parent_path: bool = True) -> list:
    """returns only ONE level sub directories"""
    p = path if isinstance(path, Path) else Path(path)

    return [p / file_name if include_parent_path else
            file_name for file_name in listdir(p) if not isfile(p / file_name)]


def get_file_name_list_in_dir(path: Union[Path, str], include_parent_path=True, valid_extension: list = None) -> list:
    """returns file names only in ONE level sub directories"""
    p = path if isinstance(path, Path) else Path(path)

    return [
        p / file_name if include_parent_path else
        file_name for file_name in listdir(p) if
        isfile(p / file_name) and
        (valid_extension is None or Path(file_name).suffix in valid_extension)
    ]


def get_sub_dir_and_file_dict_in_dir(path: Union[Path, str], valid_extension: list = None) -> dict:
    """returns all the file names Recursively in ALL sub directories"""
    p = path if isinstance(path, Path) else Path(path)

    dir_file_dict = {}

    for f in os.walk(p):
        if Path(f[0]) not in dir_file_dict:
            dir_file_dict[Path(f[0])] = []

        for file_name in f[2]:
            if valid_extension is None or Path(file_name).suffix in valid_extension:
                dir_file_dict[Path(f[0])].append(file_name)

        dir_file_dict[Path(f[0])].sort()

    return dir_file_dict


def get_file_path_list_in_dir_and_sub_dir(path: Union[Path, str], valid_extension: list = None) -> list:
    """returns a list of all the file names Recursively in ALL sub directories"""
    sub_file_path_list = list()

    for f in os.walk(path):
        for file_name in f[2]:
            if valid_extension is None or Path(file_name).suffix in valid_extension:
                sub_file_path_list.append(Path(f[0]) / file_name)

    return sub_file_path_list


def get_line_list_from_text(path: Union[Path, str], print_lines: bool = False, remove_rear_enter: bool = True) -> list:
    assert path_exists(path)

    string_list = []
    with open(path, "r") as text_file:
        for i, line in enumerate(text_file):
            string_list.append(line[:-1] if len(line) > 0 and remove_rear_enter and line[-1] == "\n" else line)
            if print_lines:
                print("line_{:4d}: {}".format(i+1, line))

    return string_list


def safe_copy_dir(src: Union[Path, str], dst: Union[Path, str]):
    assert path_exists(src)

    copytree(src, dst)


def safe_copy_file(src: Union[Path, str], dst: Union[Path, str], override=False):
    assert path_exists(src)

    d = dst if isinstance(dst, Path) else Path(dst)
    ensure_path(d.parent)

    if override:
        copyfile(src, dst)

        return 0

    elif not path_exists(dst):
        copyfile(src, dst)

        return 1

    else:
        if not images_identical(src, dst):
            print(f"{src} and\n{dst} not identical")

            return 0


def delete_file(path: Union[Path, str]):
    assert path_exists(path)

    os.remove(path)


def write_file(context_in: Any, path: Union[Path, str], append: bool = False, print_log: bool = False):
    p = path if isinstance(path, Path) else Path(path)

    ensure_path(p.parent)

    file = open(p, "a+" if append else "w")
    context = json.dumps(context_in, indent=4) \
        if isinstance(context_in, dict) or isinstance(context_in, list) \
        else context_in

    if context_in is not None:
        file.write("{}\n".format(context))

    if print_log:
        print("'{}' is written to {}".format(context, p))

    file.close()


def write_log(log: Any, path: Union[Path, str], print_log: bool = False):
    p = path if isinstance(path, Path) else Path(path)

    ensure_path(p.parent)

    file = open(p, 'a+')
    file.writelines("{} | {}\n".format(datetime.datetime.now(), log))
    if print_log:
        print("\"{} | {}\" is written to {}\n".format(datetime.datetime.now(), log, p))
    file.close()


def write_file_decorator(arg):
    """if only a path is input, MUST do it as a tuple: ("your/path/file/to/write",)"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            context_to_write = fn(*args, **kwargs)
            write_file(context_to_write, path, append, print_log)
            return context_to_write
        return wrapper

    if callable(arg):
        return decorator(arg)
    else:
        path = arg[0] if len(arg) > 0 else Path("./log.txt")
        append = arg[1] if len(arg) > 1 else False
        print_log = arg[2] if len(arg) > 2 else False
        return decorator


def write_log_decorator(arg):
    """if only a path is input, MUST do it as a tuple: ("your/path/file/to/write",)"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            log = fn(*args, **kwargs)
            write_log(log, path, print_log)
            return log
        return wrapper

    if callable(arg):
        return decorator(arg)
    else:
        path = arg[0] if len(arg) > 0 else Path("./log.txt")
        print_log = arg[1] if len(arg) > 1 else False
        return decorator


def time_stamp_range_decorator(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        time_stamp_start = datetime.datetime.now()
        res = fn(*args, **kwargs)
        time_stamp_end = datetime.datetime.now()

        return "\n{}\n".format("-" * 100) + \
               f"{time_stamp_start}: {fn} starts\n" \
               f"running for: {time_stamp_end - time_stamp_start}\n" \
               f"returns: {res}\n" \
               f"{time_stamp_end}: {fn} ends\n" + \
               "{}\n".format("-" * 100)

    return wrapper




