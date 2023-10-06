"""
giulbia github baby_cry_detection repository를 통해 소리 데이터를 받을 수 있다. 모든 데이터를 사용하는 것이 아닌 아이의 웃음소리 데이터만을 사용 할 것이다. 데이터는 아래 홈페이지에서 내려받을 수 있다.

https://github.com/giulbia/baby_cry_detection
"""

# Load packages
import os
import sys
import pandas as pd


origin_file_path = "/Users/jaewone/Downloads/baby_cry_detection-master/data/903 - Baby laugh"

main_path = os.path.join(os.getcwd().rsplit(
    'baby-cry-classification')[0], 'baby-cry-classification')
data_path = os.path.join(main_path, 'data')
csv_path = os.path.join(main_path, 'origin_data_info.csv')


sys.path.append(main_path)
from utils.os import *


def get_file_list(path: str) -> list[str]:
    audio_list = []
    for file_path, file in file_itorator(path, include='.wav'):
        audio_list.append(os.path.join(file_path, file))
    return audio_list


def get_data_as_df(file_path_list: list[str]) -> pd.DataFrame:
    df = pd.DataFrame(columns=['state', 'gender',
                      'age', 'file', 'detail', 'source'])

    df['file'] = file_path_list
    df['state'] = 'happy'
    df['source'] = 'giulbia'
    df['gender'] = df['age'] = df['detail'] = ''

    return df


def get_giulbia_data(
        origin_file_path: str,
        data_path: str,
        csv_path: str):
    # get audio list from path
    baby_audio_list = get_file_list(origin_file_path)

    # create dataframe with audio path list
    df = get_data_as_df(baby_audio_list)

    # move files
    move_files(origin_file_path, data_path, include='.wav')

    # update file path
    df['file'] = df['file'].str.replace(f'{origin_file_path}/', '')

    # Append to csv
    origin_df = pd.read_csv(csv_path, index_col=0).fillna('')
    origin_df = pd.concat([origin_df, df]).reset_index(drop=True)
    origin_df.to_csv(csv_path)


if __name__ == '__main__':
    get_giulbia_data(origin_file_path, data_path, csv_path)
