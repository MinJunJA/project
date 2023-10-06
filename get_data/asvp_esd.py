"""
## ASVP-ESD 데이터셋을 가져와보자.

데이터셋은 아래 홈페이지에서 받을 수 있다.

https://github.com/HLTSingapore/Emotional-Speech-Data

문서의 설명으로부터 파일 이름에 따른 정보를 얻을 수 있었다. 이를 기반으로 아이의 울음소리에 대한 음성만을 추출한 뒤 csv 파일을 통해 정보를 저장하자.

아래는 파일 이름에 따른 정보 예시이다.

**03-01-06-01-02-12-02-01-01-16.wav**

1. 오디오 전용 (03)

2. 음향기기 사용 (01)

3. 두려움 (06)

4. 강한 목소리 (01)

5. Statement (02)

6. 남자(짝수는 남, 홀수는 여)

7. 나이는 20세에서 64세 사이

8. 출처-웹사이트

9. 언어-중국어

<br>

3번인 감정, 6번인 성별 또한 추출할 것이다. 감정과 성별에 대한 정보는 아래와 같다.

4세 이하의 나이는 구별하고 있지 않다.

<br>

**감정**

- 01 = 지루함, 한숨

- 02 = 중립, 진정

- 03 = 행복, 웃음

- 04 = 슬프다, 울다

- 05 = 분노, 투덜거림, 좌절

- 06 = 두렵다, 비명을 지르다, 당황하다

- 07 = 혐오, 혐오, 경멸

- 08 = 놀라다, 숨이 막히다, 놀라다

- 09 = 흥분

- 10 = 즐거움

- 11 = 고통, 신음

- 12 = 실망, 반대

- 13 = 호흡

<br>

**성별**

짝수는 남성, 홀수는 여성으로 구분한다. 숫자의 의미는 명시되어 있지 않다.

"""

# Load packages
import os
import sys
import numpy as np
import pandas as pd


origin_file_path = '/Users/jaewone/Downloads/ASVP-ESD-Update/Bonus'

main_path = os.path.join(os.getcwd().rsplit(
    'baby-cry-classification')[0], 'baby-cry-classification')
data_path = os.path.join(main_path, 'data')
csv_path = os.path.join(main_path, 'origin_data_info.csv')


sys.path.append(main_path)
from utils.os import *


def get_feel(feel_code):
    if feel_code == '01':
        return 'bored'
    elif feel_code == '03':
        return 'happy'
    elif feel_code == '04':
        return 'sad'
    elif feel_code == '06':
        return 'fearful'
    elif feel_code == '11':
        return 'pain'
    elif feel_code == '17':
        return 'disgust'
    elif feel_code == '02':
        return 'calm'
    return 'calm'


def get_detail_feel(feel):
    if not type(feel) == str:
        return ''

    if (feel == '77'):
        return 'high_noise'
    if feel == '66':
        return 'max-sound'

    try:
        num = int(feel)
    except:
        return ''

    if num < 10:
        return ''

    state_num = num % 10
    if state_num == 4:
        return 'sad'
    if state_num == 5:
        return 'happy'
    if state_num == 6:
        return 'fearful'
    if state_num == 7:
        return 'disgust'
    if state_num == 8:
        return 'surprise'
    return ''


def combin_path(
    p1, p2): return f'{p1}/{p2}' if p1 != '' and p2 != '' else p1 + p2


def get_baby_audio_list(origin_file_path: str):
    baby_audio_list = []

    for path, file in file_itorator(origin_file_path, include='.wav'):
        info = file.rsplit('.', 1)[0].split('-')
        baby_audio_list.append(
            [info[2], info[5], '-'.join(info[9:]), os.path.join(path, file)])

    return baby_audio_list


def trans_detail(ser: pd.Series):
    return (ser.str.split('-', expand=True)
            .applymap(get_detail_feel)
            .apply(lambda row: combin_path(row[0], row[1]), axis=1))


def get_asvp_esd_data(
        origin_file_path: str,
        data_path: str,
        csv_path: str):
    # Get baby audio file path list
    baby_audio_list = get_baby_audio_list(origin_file_path)

    # trans data
    feel_info = [get_feel(info[0]) for info in baby_audio_list]
    gender_info = ['m' if int(info[1]) %
                   2 == 0 else 'f' for info in baby_audio_list]
    detail_info = [''.join(info[2][:5]) for info in baby_audio_list]

    # trans to dataframe
    df = pd.DataFrame(list(zip(feel_info, gender_info, detail_info, [
        info[3] for info in baby_audio_list])), columns=['state', 'gender', 'detail', 'file'])

    # move files
    move_files(origin_file_path, data_path, extension=['.wav'])

    # fill data
    df['detail'] = trans_detail(pd.Series(df.detail.values))
    df['file'] = df['file'].str.replace(origin_file_path, '').str.replace(
        '|'.join([f'/actor_{folder_name}/' for folder_name in ['50', '150', '200']]), '')
    df['age'] = ''
    df['source'] = 'asvp-esd'

    # append to csv
    origin_df = pd.read_csv(csv_path, index_col=0)
    origin_df = pd.concat([origin_df, df]).reset_index(drop=True)
    origin_df.to_csv(csv_path)


if __name__ == '__main__':
    get_asvp_esd_data(origin_file_path, data_path, csv_path)
