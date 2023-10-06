## 청각장애인 부모를 위한 아기 울음소리 감지 및 범주 분류

### 아기 울음소리 감지 및 범주 분류 모델

- 소속: 서울과학기술대학교 데이터청년 캠퍼스 01조

- 팀원: 권정연, 강근희, 곽재원, 고은아, 장민준, 신정아

<br>

### Overview

- 데이터 전처리 프로세스는 trans_data/trans_data.ipynb 를 통해 진행됨.

- 아기울음 소리 감지를 위해 YamNet이 사용되었으며 detect_baby_cry/main.py 를 통해 YamNet의 사용 예시를 확인 할 수 있다.

- 아기울음 소리 분류를 위해 사용된 모델은 ResNet50이며 model/resnet/resnet.ipynb 를 통해 진행됨.

<br>

### 파일 구성

#### 데이터셋 구성

- origin_data : 본 프로젝트에 사용된 오리지널 데이터셋

- data : 음성의 파워를 측정하여 패턴을 추출하는 것에 초점을 두어 전처리된 데이터셋.

- origin_data_info.csv : origin_data에서 각 파일에 대한 state, age와 같은 부과 정보를 포함하는 csv

<br>

#### 데이터 전처리

- get_data : 각각의 원본 데이터를 받아 state 표현 방식 통일과 같은 origin_data를 구성하는 과정을 담은 폴더. 자세한 설명은 get_data README를 참고해주세요.

- trans_data : 데이터 전처리에 사용된 함수들과 과정을 담은 폴더. 자세한 설명은 trans_data의 README를 참고해주세요.

<br>

#### 모델

- detect_baby_cry : 아기 울음소리를 감지하는 모델로 YamNet에 대한 내용을 포함한다.

- model : 아기의 울음소리 범주를 분류하는 모델로 LSTM, CRNN, ResNet50, 등에 대한 내용을 포함한다.

<br>

#### 기타

- utils : 음성과 OS에 대한 유틸리티 함수를 제공한다.
# project
