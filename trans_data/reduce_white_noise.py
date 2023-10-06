from scipy.io import wavfile
from typing import Optional
import noisereduce as nr


def reduced_base_noise(file_path: str,
                       output_path: Optional[str] = None,
                       inplace: bool = False):
    """
    noisereduce 라이브러리를 이용하여 기본적인 노이즈를 감소시킨다.

    Parameters:
        * file_path : 처리하고자 하는 파일의 경로
        * output_path : 처리한 결과를 저장하고자 하는 파일 경로. 없을 경우 file_path의 파일을 덮어쓴다.
        * inplace : 원본 데이터(file_path)를 처리한 파일로 덮어쓴다.

    Returns: None
    """

    if inplace == False and output_path == None:
        raise ValueError(f'output path must be defined if inplace is False.')

    if output_path == None or inplace == True:
        output_path = file_path

    # load data
    rate, data = wavfile.read(file_path)

    # perform noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write(output_path, rate, reduced_noise)
