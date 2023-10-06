"""
## iFLYTEK 아기 울음 인식 챌린지 데이터 세트

데이터에 대한 추가적인 설명은 없으며 파일 이름을 통해 라벨링되어 있다. 

데이터셋은 아래 홈페이지에서 다운 받을 수 있다. 데이터셋 중 라벨링되어 있는 train 부분만을 데이터로 사용한다.

https://aistudio.baidu.com/aistudio/datasetdetail/41960
"""

# Load packages
import os
import sys
import pandas as pd


origin_file_path = "/Users/jaewone/Downloads/iflytek/train"
label_list = ['hug', 'diaper', 'hungry', 'sleepy', 'awake', 'uncomfortable']

main_path = os.path.join(os.getcwd().rsplit(
    'baby-cry-classification')[0], 'baby-cry-classification')
data_path = os.path.join(main_path, 'data')
csv_path = os.path.join(main_path, 'origin_data_info.csv')


sys.path.append(main_path)
from utils.os import *


def get_df_from_data(origin_file_path: str):
    file_list = []
    state_list = []

    for label in label_list:
        label_folder_path = os.path.join(origin_file_path, label)
        for file in os.listdir(label_folder_path):
            if file.rsplit('.')[1] == 'wav':
                file_list.append(os.path.join(label_folder_path, file))
                state_list.append(file.split('_', 1)[0])

    # Create df
    df = pd.DataFrame(list(zip(file_list, state_list)),
                      columns=['file', 'state'])
    df['source'] = 'iFLYTEK'
    df['gender'] = df['age'] = df['detail'] = ''

    return df


def get_iFLYTEK_data(
        origin_file_path: str,
        data_path: str,
        csv_path: str):
    # get df from data
    df = get_df_from_data(origin_file_path)

    # move files
    move_files(origin_file_path, data_path, include='.wav')

    # Update file path
    df['file'] = df['file'].str.replace(origin_file_path, '').str.replace(
        '|'.join([f'/{label}/' for label in label_list]), '')

    # Append to csv
    origin_df = pd.read_csv(csv_path, index_col=0).fillna('')
    origin_df = pd.concat([origin_df, df]).reset_index(drop=True)
    origin_df.to_csv(csv_path)


if __name__ == '__main__':
    get_iFLYTEK_data(origin_file_path, data_path, csv_path)
