import numpy as np
import numpy.typing as npt


def add_zeros(x: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
    """
    Add zeros between values of given array
    :param x: array,
    :return: array with zeros inserted
    """
    y: npt.NDArray[np.int_] = np.zeros((x.shape[0], 1), dtype=np.int_)
    x = x.reshape((x.shape[0], 1))
    # print(x)
    # print(y)
    answer = np.concatenate((x, y), axis=1)
    # print(answer)
    # print(answer.reshape(x.shape[0]*2))
    return answer.reshape(x.shape[0]*2)[:-1]
