import os
import sys
import numpy as np
import pandas as pd


main_path = os.path.join(os.getcwd().rsplit(
    'baby-cry-classification')[0], 'baby-cry-classification')
data_path = os.path.join(main_path, 'data')
csv_path = os.path.join(main_path, 'origin_data_info.csv')


sys.path.append(main_path)
from utils.os import *
from utils.sound import *

from asvp_esd import get_asvp_esd_data
from donateacry_corpus import get_donateacry_corpus_data
from giulbia import get_giulbia_data
from iFLYTEK import get_iFLYTEK_data
from wojiaoguodekai import get_wojiaoguodekai_data


def get_total_data():
    # create folder if not exist
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    # create csv if not exist
    if not os.path.exists(csv_path):
        df = pd.DataFrame(columns=['state', 'gender',
                                   'age', 'source', 'file', 'detail'])
        df.to_csv(csv_path)

    # get data
    get_asvp_esd_data(
        '/Users/jaewone/Downloads/ASVP-ESD-Update/Bonus', data_path, csv_path)
    get_donateacry_corpus_data(
        "/Users/jaewone/Downloads/donateacry_corpus_cleaned_and_updated_data", data_path, csv_path)
    get_giulbia_data(
        "/Users/jaewone/Downloads/baby_cry_detection-master/data/903 - Baby laugh", data_path, csv_path)
    get_iFLYTEK_data("/Users/jaewone/Downloads/iflytek/train",
                     data_path, csv_path)
    get_wojiaoguodekai_data(
        "/Users/jaewone/Downloads/DatasetId_205704_1663556775", data_path, csv_path)

    # add duartion column
    df['duration'] = df['file'].apply(
        lambda file: get_duration(os.path.join(data_path, file)))

    # check csv
    df = pd.read_csv(csv_path, index_col=0, dtype={
        'state': 'category',
        'gender': 'category',
        'age': 'category',
        'source': 'category',
    })

    print(df.info())
    print(df.tail(3))


if __name__ == '__main__':
    get_total_data()
