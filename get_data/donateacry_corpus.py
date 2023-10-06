"""
## 개요

데이터 설명으로부터 파일 이름은 다음과 같은 내용을 포함함을 확인할 수 있다.

* ID
* Record time
* Record_mobile_version
* gender
* age(week)
* status

예를 들어 0D1AD73E-4C5E-45F3-85C4-9A3CB71E8856-1430742197-1.0-m-04-hu.caf 파일명은 아래와 같이 해석될 수 있다.

- 샘플은 고유 ID가 0D1AD73E-4C5E-45F3-85C4-9A3CB71E8856인 앱 인스턴스로 기록되었다. 이 ID는 설치 시 생성되므로 장치나 사용자가 아닌 설치된 인스턴스를 식별한다.
- 기록은 1430742197(유닉스 시간 에포크)에 이루어졌으며 이는 2015년 5월 4일 월요일 12:23:17 GMT로 변환된다.
- 모바일 앱 버전 1.0 사용함.
- gender는 male.
- 아기는 사용자에 따라 생후 0-4주.
- 울음의 의심되는 이유는 배고픔.

자세한 변수에 대한 설명은 아래와 같다.

* **Gender**
  - *m* - male
  - *f* - female

* **Age**
  - *04* - 0 to 4 weeks old
  - *48* - 4 to 8 weeks old
  - *26* - 2 to 6 months old
  - *72* - 7 month to 2 years old
  - *22* - more than 2 years old

* **Reason**
  - *hu* - hungry
  - *bu* - needs burping
  - *bp* - belly pain
  - *dc* - discomfort
  - *ti* - tired
"""

# Load packages
import os
import sys
import pandas as pd


main_path = os.path.join(os.getcwd().rsplit(
    'baby-cry-classification')[0], 'baby-cry-classification')
data_path = os.path.join(main_path, 'data')
csv_path = os.path.join(main_path, 'origin_data_info.csv')

origin_file_path = "/Users/jaewone/Downloads/donateacry_corpus_cleaned_and_updated_data"
label_list = ['belly_pain', 'discomfort', 'burping', 'tired', 'hungry']

sys.path.append(main_path)
from utils.os import *


def get_data_df(label: str, df_columns: list[str]) -> pd.DataFrame:
    files_path = os.path.join(origin_file_path, label)
    names = [name.rsplit('.', 1)[0].rsplit(
        '-', 3)[1:] + [os.path.join(origin_file_path, label, name)] for name in os.listdir(files_path)]
    return pd.DataFrame(names, columns=df_columns)


def get_total_data() -> pd.DataFrame:
    df_columns = ['gender', 'age', 'state', 'file']
    df = pd.DataFrame(columns=df_columns)

    for label in label_list:
        df = pd.concat([df, get_data_df(label, df_columns)])

    df['source'] = 'donate_a_cry'
    df['detail'] = ''
    df = df.reset_index(drop=True)

    return df


def get_full_state_name(state):
    if state == "bp":
        return 'belly_pain'
    if state == "dc":
        return 'discomfort'
    if state == "bu":
        return 'burping'
    if state == "ti":
        return 'tired'
    if state == "hu":
        return 'hungry'
    # if state == "ch":
    return state


def get_donateacry_corpus_data(
        origin_file_path: str,
        data_path: str,
        csv_path: str):
    # get data
    df = get_total_data()

    # move files
    move_files(origin_file_path, data_path, include='.wav')

    # Update file path in datframe
    df['file'] = df['file'].str.replace(origin_file_path, '').str.replace(
        '|'.join([f'/{label}/' for label in label_list]), '')

    # get full state name
    df['state'] = df['state'].apply(get_full_state_name)

    # append to csv
    origin_df = pd.read_csv(csv_path, index_col=0)
    origin_df = pd.concat([origin_df, df])
    origin_df.to_csv(csv_path)


if __name__ == '__main__':
    get_donateacry_corpus_data(origin_file_path, data_path, csv_path)
