from utils.os import remove_file
import numpy as np
import os
import librosa
from scipy.io import wavfile
from typing import Optional, Union
import wave


def create_split_audio(file_path: str,
                       split_sec: int,
                       output_path: Optional[str] = None,
                       inplace: bool = False):

    if inplace == False and output_path == None:
        raise ValueError(f'output path must be defined if inplace is False.')

    if inplace:
        output_path = file_path.rsplit('/', 1)[0]

    with wave.open(file_path, 'rb') as wf:
        n_channels, sampwidth, framerate, n_frames, comptype, compname = wf.getparams()

        # 분활할 초에 따른 전체 프레임수
        frames_for_split_sec = split_sec * framerate

        # 나누어야 하는 파일의 수
        num_segments = n_frames // frames_for_split_sec

        # 파일명
        base_name = os.path.basename(file_path).replace(".wav", "")

        saved_files = []
        for i in range(num_segments):
            frames = wf.readframes(frames_for_split_sec)

            # Create a new wave file for the segment
            new_file_name = f"{base_name}_{i + 1}.wav"
            new_file_path = os.path.join(output_path, new_file_name)

            with wave.open(new_file_path, 'wb') as segment_wf:
                segment_wf.setnchannels(n_channels)
                segment_wf.setsampwidth(sampwidth)
                segment_wf.setframerate(framerate)
                segment_wf.writeframes(frames)

            saved_files.append(new_file_name)

    if inplace:
        remove_file(file_path)

    return saved_files


def split_audio_list_in_sec(file_list: list[str],
                            split_sec: Union[int, float],
                            output_path: Optional[str] = None,
                            inplace: bool = False):

    if inplace == False and output_path == None:
        raise ValueError(f'output path must be defined if inplace is False.')

    if output_path != None:
        if os.path.exists(output_path):
            raise OSError(f'path {output_path} already exists.')
        else:
            os.mkdir(output_path)

    saved_files_list_wave = []
    for wav_file in file_list:
        saved_files_list_wave.extend(
            create_split_audio(wav_file, split_sec, output_path, inplace))

    return saved_files_list_wave


# 각 파일의 2초부터 7초 사이의 음성을 추출한다.
def split_audios(file_list: list[str],
                 start_time: float = 0,
                 end_time: float = 0,
                 inplace: bool = False,
                 output_path: Optional[str] = None):
    """
    파일 리스트의 음성 파일들을 start_time부터 end_time까지 자른다.

    Parameters:

      file_list : 변환할 파일의 경로 리스트. wav 파일만 가능하다.

      start_time : 자르기를 시작하는 시점(초)

      end_time : 자르기를 종료하는 시점(초)

      inplace : True일 경우 원본 파일을 덮어쓴다.

      output_path : 변환된 파일을 저장할 폴더 경로

    """

    if inplace == False and output_path == None:
        raise ValueError(f'output path must be defined if inplace is False.')

    if end_time - start_time <= 0:
        raise ValueError(f'Splited sound must be more than 0 second.')

    # output_path 경로(폴더)가 없을 경우 생성한다.
    if output_path != None:
        if os.path.exists(output_path):
            raise OSError(f'output path {output_path} already exists.')
        else:
            os.makedirs(output_path)

    # 파일을 자른다.
    for file_path in file_list:

        # 파일의 정보를 읽어온다.
        y, sr = librosa.load(file_path, sr=None)

        # 음성 자르기
        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)
        segmented_audio = y[start_sample:end_sample]

        # 저장
        segmented_audio = np.array(segmented_audio * (2**15), dtype=np.int16)
        output_file_path = file_path if inplace else os.path.join(
            output_file_path, file_path.rsplit('/', 1)[1])
        wavfile.write(output_file_path, sr, segmented_audio)
