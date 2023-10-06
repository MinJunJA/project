from typing import Optional
import wave
import numpy as np

from utils.os import *
from utils.sound import *


def detect_non_silence(audio_data: np.ndarray, threshold: float, frame_size: int) -> list[int]:
    """
    오디오 신호에서 무음이 아닌 섹션의 시작과 끝을 감지한다.

    Parameters:
        - audio_data (numpy.ndarray): 묵음을 감지해야 하는 오디오 데이터.
        - threshold (float): 오디오가 무음으로 간주되는 에너지 임계값.
        - frame_size (int): 오디오 에너지의 이동 평균을 계산하기 위해 고려할 샘플 수.

    Returns:
        - start (int): 비침묵 섹션의 시작 샘플.
        - end (int): non-silence 섹션의 엔딩 샘플.
    """

    moving_avg = np.convolve(audio_data, np.ones(
        (frame_size,))/frame_size, mode='valid')
    non_silence = np.where(moving_avg > threshold)[0]

    start = non_silence[0]
    # compensate for the 'valid' mode in convolution
    end = non_silence[-1] + frame_size

    return start, end


def trim_audio(file_path: str, output_path: Optional[str] = None, inplace: bool = False, frame_size=5000):
    """
    오디오의 앞뒤에 존재하는 화이트 노이즈를 제거한다.
    화이트 노이즈는 음성의 전체 에너지의 하위 10%에 해당하는 시점으로 정의한다.

    Parameters:
        * file_path : 처리하고자 하는 파일의 경로
        * output_path : 처리한 결과를 저장하고자 하는 파일 경로. 없을 경우 file_path의 파일을 덮어쓴다.
        * inplace : 원본 데이터(file_path)를 처리한 파일로 덮어쓴다.

    Returns: None
    """

    if inplace == False and output_path == None:
        raise ValueError(f'output path must be defined if inplace is False.')

    # wav 파일을 읽어온다.
    with wave.open(file_path, "r") as file:
        params = file.getparams()
        n_frames = params[3]
        audio_data = file.readframes(n_frames)
        wave_data = np.frombuffer(audio_data, dtype=np.int16)

    # 오디오 시그널을 통한 에너지 계산
    energy = np.abs(wave_data)

    # 백색 잡음을 분류하기 위한 임계값을 설정.
    # 전체 에너지의 하위 10%에 10을 곱하여 임계값을 설정하였으나 추가적은 고민이 필요하다.
    threshold = np.percentile(energy, 10) * 10

    # Use a larger frame size to get a moving average of the audio energy
    frame_size = frame_size
    error_files = []
    try:
        start, end = detect_non_silence(energy, threshold, frame_size)
        trimmed_wave_data = wave_data[start:end]
    except:
        trimmed_wave_data = wave_data
        error_files.append(file_path)
    # print(start, end)

    # trim된 numpy array를 wav 파일로 저장한다.
    if inplace or output_path == None:
        remove_file(file_path)
        output_path = file_path
    with wave.open(output_path, "w") as out_file:
        out_file.setparams(params)
        out_file.writeframes(trimmed_wave_data.tobytes())

    return error_files
