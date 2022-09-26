def find_value(nums: list[int] | range, value: int) -> bool:
    """
    Find value in sorted sequence
    :param nums: sequence of integers. Could be empty
    :param value: integer to find
    :return: True if value exists, False otherwise
    """
    left_index = -1
    right_index = len(nums)
    while right_index - left_index > 1:
        mid_index = (right_index + left_index)//2
        if nums[mid_index] == value:
            return True
        if nums[mid_index] < value:
            left_index = mid_index
        else:
            right_index = mid_index
    return False
