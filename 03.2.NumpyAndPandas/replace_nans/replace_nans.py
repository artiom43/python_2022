import numpy as np
import numpy.typing as npt


def replace_nans(matrix: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]:
    """
    Replace all nans in matrix with average of other values.
    If all values are nans, then return zero matrix of the same size.
    :param matrix: matrix,
    :return: replaced matrix
    """
    bool_m = np.isnan(matrix)
    shape_arr = matrix.shape
    # print(np.count_nonzero(bool_m))
    if np.count_nonzero(bool_m) == shape_arr[0]*shape_arr[1]:
        return np.nan_to_num(matrix, nan=0)
    # print(np.mean(matrix, where=bool_m))
    # print(np.nan_to_num(matrix, nan=np.mean(matrix)))
    # return np.nan_to_num(matrix, nan=np.nanmean(matrix, dtype=np.float_))
    value = np.nanmean(matrix)
    np.place(matrix, bool_m, value)
    # print(matrix)
    return matrix
