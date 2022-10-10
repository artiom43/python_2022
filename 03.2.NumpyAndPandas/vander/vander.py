import numpy as np
import numpy.typing as npt


def vander(array: npt.NDArray[np.float_ | np.int_]) -> npt.NDArray[np.float_]:
    """
    Create a Vandermod matrix from the given vector.
    :param array: input array,
    :return: vandermonde matrix
    """
    array = array.reshape((array.shape[0], 1))
    print(array.shape[1])
    ar_zer = np.zeros((array.shape[0]))
    ar_ones = np.ones((array.shape[0]))*(array.shape[0] - 1)
    print(ar_zer, ar_ones)
    answer = np.logspace(ar_zer, ar_ones, num=array.shape[0], base=array, axis=1)
    print(answer)
    return answer
