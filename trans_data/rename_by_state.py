from trans_data.get_state_list import get_state_list_from_dir_name
from utils.os import rename_by_keyword
import os
from typing import Optional


def rename_files_by_state(data_path: str,
                          state_list: Optional[list[str]] = None,
                          include_etc=False) -> list[str]:
    """
    state에 따라 파일의 이름을 변경한다.

    Parameters:
        data_path : 파일의 경로

        state_list=None : state 리스트를 받을 경우 state_list가 포함하는 state 폴더의 파일들만 이름을 변경한다.

        include_etc=False : True일 경우 etc 폴더를 state에 포함한다.

    Returns: 변환된 파일 경로 리스트
    """

    if not os.path.exists(data_path):
        raise OSError(f'data path {data_path} not exist.')

    # Get state list if not exist
    if state_list == None:
        state_list = get_state_list_from_dir_name(
            data_path, include_etc=include_etc)
    else:
        for state in state_list:
            if not os.path.exists(os.path.join(data_path, state)):
                raise OSError(
                    f"The path corresponding to state '{state}' does not exist.")

    # rename files
    renamed_file_list = []
    for state in state_list:
        state_path = os.path.join(data_path, state)
        file_path_list = [os.path.join(state_path, file)
                          for file in os.listdir(state_path)]
        renamed_file_list += rename_by_keyword(file_path_list, state)

    return renamed_file_list
