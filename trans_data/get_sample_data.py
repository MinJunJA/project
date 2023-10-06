from trans_data.get_state_list import get_state_list_from_dir_name
from utils.os import *
import os
from typing import Optional
from random import sample, seed, choices, shuffle
from math import isclose


def get_state_samples(data_path: str,
                      state_list: Optional[list[str]] = None,
                      n_extract: int = 100,
                      rand_seed: int = 123) -> list[str]:
    """
    각각의 state에서 n개의 무작위 파일을 선택하여 경로를 반환한다.

    Parameters:

        * data_path : 파일의 경로

        * state_list=None : state 리스트를 받을 경우 state_list가 포함하는 state 폴더의 파일들만 이름을 변경한다.

        * n_extract=100 : 각각의 state 별 추출할 파일 개수. 만약 n_etract 보다 파일 개수가 부족하다면 파일의 개수 만큼만 추출한다.

        * rand_seed=123 : 난수를 생성하는 시드값으로 동일한 시드값은 동일한 결과를 보장한다.

    Returns: 랜덤 추출한 파일의 경로 리스트
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

    seed(rand_seed)
    file_list = []
    for state in state_list:
        state_file_list = [os.path.join(data_path, state, file) for file in os.listdir(
            os.path.join(data_path, state))]
        file_list = file_list + (sample(state_file_list, k=n_extract)
                                 if len(state_file_list) > n_extract else state_file_list)

    return file_list


def extract_state_sample(data_path: str,
                         output_dir: str,
                         n_extract: int = 100,
                         rand_seed: int = 123,
                         state_list: Optional[list[str]] = None,
                         with_dir: bool = True) -> list[str]:
    """
    각각의 state에서 n개의 무작위 파일을 추출한다.

    Parameters:

        * data_path : 파일의 경로

        * output_dir : sample 파일들을 저장할 폴더 경로. 만약 경로가 이미 존재 할 경우 예외를 발생시키며 경로가 없으면 생성한다.

        * n_extract=100 : 각각의 state 별 추출할 파일 개수. 만약 n_etract 보다 파일 개수가 부족하다면 파일의 개수 만큼만 추출한다.

        * rand_seed=123 : 난수를 생성하는 시드값으로 동일한 시드값은 동일한 결과를 보장한다.

        * state_list=None : state 리스트를 받을 경우 state_list가 포함하는 state 폴더의 파일들만 이름을 변경한다.

        * with_dir=True : False일 경우 output_path에 state에 따른 폴더 구분 없이 데이터를 추출한다.

    Returns: 랜덤 추출하여 저장된 파일의 경로 리스트
    """

    # Check output_dir exist.
    if os.path.exists(output_dir):
        raise OSError(f'path {output_dir} already exist.')
    else:
        os.mkdir(output_dir)

    # Get state list if not exist
    if state_list == None:
        state_list = get_state_list_from_dir_name(data_path)
    else:
        for state in state_list:
            if not os.path.exists(os.path.join(data_path, state)):
                raise OSError(
                    f"The path corresponding to state '{state}' does not exist.")

    # Create folder of state if with_dir is True
    if with_dir:
        for state in state_list:
            os.mkdir(os.path.join(output_dir, state))

    # Extract n sample of state
    sample_data_list = get_state_samples(
        data_path, state_list, n_extract, rand_seed)

    # Copy files with sample data list
    output_file_list = []
    for file in sample_data_list:
        if with_dir:
            _, dir, filename = file.rsplit('/', 2)
            output_file = os.path.join(output_dir, dir, filename)
            output_file_list.append(output_file)
            copy_file(file, output_file)
        else:
            output_file = os.path.join(output_dir, file.rsplit('/', 1)[1])
            output_file_list.append(output_file)
            copy_file(file, output_file)

    return output_file_list


def get_sample_from_path(data_path: str,
                         n_extract: int = 100,
                         rand_seed: int = 123,
                         replace: bool = False) -> list[str]:
    """
    지정된 경로에서 n개의 무작위 파일을 선택하여 경로를 반환한다.

    Parameters:

        * data_path : 파일의 경로

        * n_extract=100 : 추출할 파일의 개수. replace가 False 이며 n_etract 보다 파일 개수가 부족하다면 파일의 개수 만큼만 추출한다.

        * rand_seed=123 : 난수를 생성하는 시드값으로 동일한 시드값은 동일한 결과를 보장한다.

        * replace : True일 경우 복원추출을 수행한다.

    Returns: 랜덤 추출한 파일의 경로 리스트
    """

    if not os.path.exists(data_path):
        raise OSError(f'path {data_path} not exist.')

    seed(rand_seed)
    file_list = [os.path.join(data_path, file)
                 for file in os.listdir(data_path)]

    if replace:
        return choices(file_list, k=n_extract)

    return sample(file_list, k=n_extract) if len(file_list) > n_extract else file_list



def extract_data_sample(data_path: str,
                        output_dir: str,
                        n_extract: int = 100,
                        rand_seed: int = 123,
                        replace: bool = False) -> list[str]:
    """
    지정된 경로에서 n개의 무작위 파일을 추출한다.

    Parameters:

        * data_path : 파일의 경로

        * output_dir : sample 파일들을 저장할 폴더 경로. 만약 경로가 이미 존재 할 경우 예외를 발생시키며 경로가 없으면 생성한다.

        * n_extract=100 : 추출할 파일의 개수. replace가 False 이며 n_etract 보다 파일 개수가 부족하다면 파일의 개수 만큼만 추출한다.

        * rand_seed=123 : 난수를 생성하는 시드값으로 동일한 시드값은 동일한 결과를 보장한다.

        * replace : True일 경우 복원추출을 수행한다.

    Returns: 랜덤 추출하여 저장된 파일의 경로 리스트
    """

    # Check output_dir exist.
    if os.path.exists(output_dir):
        raise OSError(f'path {output_dir} already exist.')
    else:
        os.mkdir(output_dir)

    # Extract n sample of state
    sample_data_list = get_sample_from_path(
        data_path, n_extract, rand_seed, replace)

    # Copy files with sample data list
    output_file_list = []
    for file in sample_data_list:
        output_file = os.path.join(output_dir, file.rsplit('/', 1)[1])
        output_file_list.append(output_file)
        copy_file(file, output_file)

    return output_file_list


def split_dataset(data: list[any],
                  train_ratio: float = 0.7,
                  val_ratio: float = 0.2,
                  test_ratio: float = 0.1,
                  rand_seed=1234):
    """
    데이터셋을 train, validation, test로 분할한다. 만약 입력된 비율의 총합이 1이 아닐 경우 에러를 발생한다.

    Parameters :
    - data : 분할하고자 하는 데이터 리스트
    - train_ratio : 분할하고자 하는 training 데이터셋 비율.
    - val_ratio : 분할하고자 하는 validation 데이터셋 비율.
    - test_ratio : 분할하고자 하는 test 데이터셋 비율.
    - rand_seed=123 : 난수를 생성하는 시드값으로 동일한 시드값은 동일한 결과를 보장한다.

    Returns : 분할된 train, validation, test data 데이터셋 리스트.
    """

    # Ensure the ratios sum to 1
    assert isclose(train_ratio + val_ratio + test_ratio,
                   1), "Ratios must sum to 1"

    # Shuffle the data
    seed(rand_seed)
    shuffle(data)

    # Get the split indices
    train_end = int(len(data) * train_ratio)
    val_end = train_end + int(len(data) * val_ratio)

    # Split the data
    train_data = data[:train_end]
    val_data = data[train_end:val_end]
    test_data = data[val_end:]

    return train_data, val_data, test_data

