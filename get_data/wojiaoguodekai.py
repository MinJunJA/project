"""
## 위쟈오구 아기 울음 인식 데이터 세트

데이터에 대한 특별한 설명은 없으나 각각의 wav의 정보를 담고있는 json 파일이 쌍을 이루어 제공된다. 

json 파일에는 각각의 라벨이 명시되어 있다.

silance 라벨은 말 그대로 조용한 배경 소리를 담고 있다. 불필요한 데이터셋이라 판단하여 제외하는 것도 고려해보자.

데이터셋은 아래 홈페이지에서 다운 받을 수 있다.

https://aistudio.baidu.com/aistudio/datasetdetail/169602
"""

# Load packages
import os
import sys
import pandas as pd
from json import load


origin_file_path = "/Users/jaewone/Downloads/DatasetId_205704_1663556775"

main_path = os.path.join(os.getcwd().rsplit(
    'baby-cry-classification')[0], 'baby-cry-classification')
data_path = os.path.join(main_path, 'data')
csv_path = os.path.join(main_path, 'origin_data_info.csv')


sys.path.append(main_path)
from utils.os import *


def get_df_from_data(origin_file_path: str):
    file_list = []
    state_list = []

    # extract data from json
    for file in os.listdir(origin_file_path):
        file_name, ex = file.rsplit('.', 1)
        if ex == 'json':
            with open(os.path.join(origin_file_path, file)) as f:
                state = load(f)['labels'][0]['name']
                wav_file_path = f'{origin_file_path}/{file_name}.wav'
                if state != '' and os.path.exists(wav_file_path):
                    file_list.append(wav_file_path)
                    state_list.append(state)

    # Create dataframe
    df = pd.DataFrame(list(zip(file_list, state_list)),
                      columns=['file', 'state'])
    df['source'] = 'wojiaoguodekai'
    df['gender'] = df['age'] = df['detail'] = ''

    return df


def get_wojiaoguodekai_data(
        origin_file_path: str,
        data_path: str,
        csv_path: str):
    # get df from data
    df = get_df_from_data(origin_file_path)

    # move files
    move_files(origin_file_path, data_path, include='.wav')

    # update file path
    df['file'] = df['file'].str.replace(f'{origin_file_path}/', '')

    # Append to csv
    origin_df = pd.read_csv(csv_path, index_col=0).fillna('')
    origin_df = pd.concat([origin_df, df]).reset_index(drop=True)
    origin_df.to_csv(csv_path)


if __name__ == '__main__':
    get_wojiaoguodekai_data(origin_file_path, data_path, csv_path)
