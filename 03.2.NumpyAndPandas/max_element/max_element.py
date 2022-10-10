import numpy as np
import numpy.typing as npt


def max_element(array: npt.NDArray[np.int_]) -> int | None:
    """
    Return max element before zero for input array.
    If appropriate elements are absent, then return None
    :param array: array,
    :return: max element value or None
    """
    bool_arr = np.concatenate((np.array([False]), np.where(array == 0, True, False)), axis=0)[0:-1]
    print(bool_arr)
    if not bool_arr.max():
        return None
    return int(np.amax(array, where=bool_arr, initial=array.min()))
