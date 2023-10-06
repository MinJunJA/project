## Detect Baby Cry

아기의 울음소리 여부를 YamNet을 이용하여 분류를 수행하는 코드.

아기 울음소리 범주 분류에 사용되는 것이 아닌 모바일에 탑재할 tflite 모델을 파이썬 환경에서 테스트 하는 것에 본 폴더의 목적이 있다.

- main.py

  YamNet을 이용하여 입력된 Wav 파일이 어느 클래스의 음성인지 판단하는 예시를 제공.

- YamNet . Models’ performance on classifying audio samples.png

  YamNet 모델의 성능 지표.

- lite-model_yamnet_tflite_1.tflite

  YamNet 모델 파일

- yamnet_class_map.csv

  YamNet에서 분류 가능한 클래스 범주를 명시해둔 csv
