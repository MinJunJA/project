from sklearn.metrics.pairwise import cosine_similarity
from typing import Optional
from tqdm import tqdm
import librosa
import numpy as np


def compute_melspectrogram(file_path: str) -> np.ndarray:
    """
    wav 파일의 멜 스펙토그램을 계산한다.

    Parameters:
        * file_path : wav 파일의 경로

    Returns:
        * 계산된 멜 스펙트럼값(numpy array)
    """
    y, sr = librosa.load(file_path)
    mels = librosa.feature.melspectrogram(y=y, sr=sr)
    return mels


def get_similarities(file_list: list[str], top_n: Optional[int] = None) -> list[str]:
    """
    파일 리스트에서 가장 유사한 n개의 파일을 반환한다.

    Parameters:
    * file_list: 분석하고자 하는 파일 경로 리스트
    * top_n: 유사한 순으로 나열했을 때 반환 할 상위 n개의 파일 리스트. 만약 top_n=None 일 경우 전체 리스트를 반환한다.

    Returns: 유사도 순으로 나열한 n개의 파일 리스트
    """

    # 멜 스펙트럼을 분석한다.
    melspectrograms = {file_path: compute_melspectrogram(
        file_path) for file_path in file_list}

    # 코사인 유사도를 측정한다.
    n = len(file_list)
    similarity_matrix = np.zeros((n, n))
    with tqdm(total=n, desc='Processing', position=0) as pbar:
        for i in range(n):
            for j in range(n):
                mels1 = melspectrograms[file_list[i]].flatten()
                mels2 = melspectrograms[file_list[j]].flatten()

                # 두 멜 스펙트럼의 크기가 다를 경우 작은 크기에 맞춘다.
                min_size = min(mels1.shape[0], mels2.shape[0])
                mels1 = mels1[:min_size]
                mels2 = mels2[:min_size]

                similarity_matrix[i, j] = cosine_similarity(
                    mels1.reshape(1, -1), mels2.reshape(1, -1))
            pbar.update(1)

    # 유사도 순으로 나열한다.
    np.fill_diagonal(similarity_matrix, 0)
    indices = np.flip(np.argsort(np.sum(similarity_matrix, axis=1)))

    return [file_list[i] for i in (indices if top_n == None else indices[:top_n])]
