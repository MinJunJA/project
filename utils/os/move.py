import os
from shutil import move
from typing import Union, Optional

from utils.os.itorate import file_itorator


# move file
def move_file(from_path: str, to_path: str):
    move(from_path, to_path)


# move files with including and excluding files from path
def move_files(from_path: str, to_path: str,
               include: Optional[Union[str, list[str]]] = None,
               exclude: Optional[Union[str, list[str]]] = None):

    for path, file in file_itorator(from_path, include, exclude):
        move(os.path.join(path, file), os.path.join(to_path, file))
