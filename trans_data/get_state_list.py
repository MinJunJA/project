import os
from typing import Optional, Union
from utils.os import file_itorator


def get_state_list_from_dir_name(data_path: str, with_path: bool = False, include_etc: bool = False) -> list[str]:
    """
    폴더 이름으로부터 state list를 추출한다.

    Parameters:
      data_path : state list를 추출할 폴더 경로

      with_path=False : True일 경우 state 폴더의 경로를 가져온다.

      include_etc=False : True일 경우 etc 폴더를 state에 포함한다.

    Returns:
      state 리스트를 반환한다.
    """
    state_list = []
    for dir in os.listdir(data_path):
        dir_path = os.path.join(data_path, dir)
        if os.path.isdir(dir_path):
            state_list.append(dir_path if with_path else dir)

    etc_path = os.path.join(data_path, 'etc')
    if include_etc == False and os.path.exists(etc_path):
        state_list.remove(etc_path if with_path else 'etc')
    return state_list


def get_state_file_list(data_path: str,
                        state_list: Optional[list[str]] = None,
                        include: Optional[Union[str, list[str]]] = None,
                        exclude: Optional[Union[str, list[str]]] = None):
    """
    각각의 state에 존재하는 모든 파일들의 경로를 반환한다.

    Parameters:

        * data_path : 파일의 경로

        * state_list=None : state 리스트를 받을 경우 state_list가 포함하는 state 폴더의 파일들만 이름을 변경한다.

    Returns: 파일의 경로 리스트
    """
    if not os.path.exists(data_path):
        raise OSError(f'path {data_path} not exist.')

    # Get state list if not exist
    if state_list == None:
        state_list = get_state_list_from_dir_name(data_path)
    else:
        for state in state_list:
            if not os.path.exists(os.path.join(data_path, state)):
                raise OSError(
                    f"The path corresponding to state '{state}' does not exist.")

    file_list = []
    for state in state_list:
        file_list.extend([os.path.join(path, file) for path, file in file_itorator(
            os.path.join(data_path, state),
            include, exclude
        )])

    return file_list
