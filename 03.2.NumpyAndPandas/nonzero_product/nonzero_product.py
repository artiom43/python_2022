import numpy as np
import numpy.typing as npt


def nonzero_product(matrix: npt.NDArray[np.int_]) -> int | None:
    """
    Compute product of nonzero diagonal elements of matrix
    If all diagonal elements are zeros, then return None
    :param matrix: array,
    :return: product value or None
    """
    array = np.diagonal(matrix)
    # print(array)
    indices = np.nonzero(array)
    # print(np.array(indices).shape)
    if np.array(indices).shape[1] == 0:
        return None
    return np.prod(array[indices])
