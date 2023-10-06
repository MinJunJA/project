import os
from typing import Union, Optional


def __format_extension(extension: Optional[Union[str, list[str]]]) -> Optional[list[str]]:
    if extension:
        if type(extension) == str:
            extension = [extension]
        extension = [ex.replace('.', '') for ex in extension]
    return extension


def __file_itorator(path: str,
                    include: Optional[list[str]] = None,
                    exclude: Optional[list[str]] = None):
    for (parent_path, dirs, files) in os.walk(path):
        for dir in dirs:
            __file_itorator(os.path.join(path, dir), include)

        for file in files:
            s = file.rsplit('.', 1)
            if len(s) == 1:
                continue
            if include and s[1] not in include:
                continue
            if exclude and s[1] in exclude:
                continue

            yield [parent_path, file]


# Itorate files with including and excluding files from path
def file_itorator(path: str,
                  include: Optional[Union[str, list[str]]] = None,
                  exclude: Optional[Union[str, list[str]]] = None):

    include = __format_extension(include)
    exclude = __format_extension(exclude)

    return __file_itorator(path, include, exclude)
