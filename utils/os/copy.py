import os
from shutil import copyfile
from typing import Union, Optional

from utils.os.itorate import file_itorator


# copy file
def copy_file(src: str, dst: str):
    if os.path.isfile(src):
        copyfile(src, dst)
    else:
        raise OSError(f'{src} is not a file')


# copy all files in path
def copy_files(src_path: str,
               dst_path: str,
               include: Optional[Union[str, list[str]]] = None,
               exclude: Optional[Union[str, list[str]]] = None):
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    for src_path, file in file_itorator(src_path, include, exclude):
        copyfile(os.path.join(src_path, file), os.path.join(dst_path, file))
