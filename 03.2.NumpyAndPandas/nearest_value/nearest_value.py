import numpy as np
import numpy.typing as npt


def nearest_value(matrix: npt.NDArray[np.float_], value: float) -> float | None:
    """
    Find nearest value in matrix.
    If matrix is empty return None
    :param matrix: input matrix
    :param value: value to find
    :return: nearest value in matrix or None
    """
    if matrix.shape[1] == 0:
        return None
    pos = np.amin(matrix, where=matrix >= value, initial=matrix.max())
    otr = np.amax(matrix, where=matrix <= value, initial=matrix.min())
    # print(pos, otr)
    if pos - value > value - otr:
        return float(otr)
    else:
        return float(pos)
