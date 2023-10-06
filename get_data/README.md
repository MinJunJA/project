## get_data 설명

본 폴더의 파일들은 데이터를 수집하고 통일하는 내용을 담고 있다.

- donate a cry dataset

- ASVP-ESD dataset

- giulbia dataset

- 위쟈오구(wojiaoguodekai) 아기 울음 인식 dataset

- iFLYTEK 아기 울음 인식 챌린지 dataset

위 5개의 데이터셋을 수집, 통일화하는 방법은 각각의 데이터셋의 이름을 가지는 파이썬 파일(.py)에 명시되어 있으며 각각의 파일을 실행시킴으로써 데이터를 수집, 통일화 할 수 있다.

이외의 파일에 대한 설명은 다음과 같다.

- get_total_data.py: 위 5가지 데이터셋에 대한 파이썬 파일을 순차적으로 실행한다.

- overview.ipynb: 수집, 통일화된 데이터를 시각화한 overview를 제공한다.

## data overview

각각의 데이터셋은 아래와 같다. 데이터에 대한 자세한 설명은 각각의 파이썬 파일에 명시되어 있다.

### data1: donate a cry dataset

donateacry_corpus_cleaned_and_updated_data 폴더의 학습 데이터만 사용한다.

https://github.com/gveres/donateacry-corpus/tree/master/donateacry_corpus_cleaned_and_updated_data

- **Age**

  - _04_ - 0 to 4 weeks old

  - _48_ - 4 to 8 weeks old

  - _26_ - 2 to 6 months old

  - _72_ - 7 month to 2 years old

  - _22_ - more than 2 years old

<br>

### data2: ASVP-ESD dataset

https://github.com/HLTSingapore/Emotional-Speech-Data

<br>

### data3: giulbia dataset

데이터셋 중 아이의 행복한 웃음소리에 해당하는 '903 - Baby laugh' 폴더의 데이터만을 사용한다.

https://github.com/gveres/donateacry-corpus/tree/master/donateacry_corpus_cleaned_and_updated_data

<br>

### data4: 위쟈오구 아기 울음 인식 dataset

silance 라벨은 말 그대로 조용한 배경 소리를 담고 있다. 불필요한 데이터셋이라 판단하여 제외하는 것도 고려해보자.

https://aistudio.baidu.com/aistudio/datasetdetail/169602

<br>

### data5: iFLYTEK 아기 울음 인식 챌린지 dataset

데이터에 대한 추가적인 설명은 없으며 파일 이름을 통해 라벨링한다.

데이터셋 중 라벨링되어 있는 train 부분만을 데이터로 사용한다.

https://aistudio.baidu.com/aistudio/datasetdetail/41960
