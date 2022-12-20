from collections.abc import Sequence


def bin_search(num: Sequence[int], value: int) -> int:
    left_border = -1
    right_border = len(num)
    while right_border > left_border + 1:
        middle_border = (left_border + right_border) // 2
        if num[middle_border] <= value:
            left_border = middle_border
        else:
            right_border = middle_border
    return left_border


def bin_search_less(num: Sequence[int], value: int) -> int:
    left_border = -1
    right_border = len(num)
    while right_border > left_border + 1:
        middle_border = (left_border + right_border) // 2
        if num[middle_border] < value:
            left_border = middle_border
        else:
            right_border = middle_border
    return left_border


def find_median(nums1: Sequence[int], nums2: Sequence[int]) -> float:
    """
    Find median of two sorted sequences. At least one of sequences should be not empty.
    :param nums1: sorted sequence of integers
    :param nums2: sorted sequence of integers
    :return: middle value if sum of sequences' lengths is odd
             average of two middle values if sum of sequences' lengths is even
    """
    index_to_find = (len(nums1) + len(nums2) + 1) // 2
    left_border = -1
    right_border = len(nums1)
    bool_t = False
    while right_border > left_border + 1:
        middle_border = (right_border + left_border) // 2
        answer_to_call = bin_search(nums2, nums1[middle_border])
        answer_to_call_less = bin_search_less(nums2, nums1[middle_border])
        if middle_border + 1 + answer_to_call + 1 < index_to_find:
            left_border = middle_border
        elif middle_border + answer_to_call_less + 2 > index_to_find:
            right_border = middle_border
        else:
            left_border = middle_border
            bool_t = True
            break
    answer_first_index = 0
    if bool_t:
        answer_first_index = nums1[left_border]
        # print("sdf")
        if (len(nums1) + len(nums2)) % 2 != 0:
            return float(answer_first_index)

    else:
        left_border = -1
        right_border = len(nums2)

        while right_border - left_border != 1:
            middle_border = (right_border + left_border) // 2
            answer_to_call = bin_search(nums1, nums2[middle_border])
            answer_to_call_less = bin_search_less(nums1, nums2[middle_border])
            # print(middle_border, left_border, right_border, answer_to_call, index_to_find)
            if middle_border + 1 + answer_to_call + 1 < index_to_find:
                left_border = middle_border
            elif middle_border + answer_to_call_less + 2 > index_to_find:
                right_border = middle_border
            else:
                left_border = middle_border
                bool_t = True
                break

        if bool_t:
            answer_first_index = nums2[left_border]
            if (len(nums1) + len(nums2)) % 2 != 0:
                return float(answer_first_index)

    index_to_find = (len(nums1) + len(nums2)) // 2 + 1
    left_border = -1
    right_border = len(nums1)
    bool_t = False
    while right_border > left_border + 1:
        middle_border = (right_border + left_border) // 2
        answer_to_call = bin_search(nums2, nums1[middle_border])
        answer_to_call_less = bin_search_less(nums2, nums1[middle_border])
        if middle_border + 1 + answer_to_call + 1 < index_to_find:
            left_border = middle_border
        elif middle_border + answer_to_call_less + 2 > index_to_find:
            right_border = middle_border
        else:
            left_border = middle_border
            bool_t = True
            break
    answer_second_index = 0
    if bool_t:
        answer_second_index = nums1[left_border]
    else:
        left_border = -1
        right_border = len(nums2)
        while right_border - left_border > 1:
            middle_border = (right_border + left_border) // 2
            answer_to_call = bin_search(nums1, nums2[middle_border])
            answer_to_call_less = bin_search_less(nums1, nums2[middle_border])
            if middle_border + 1 + answer_to_call + 1 < index_to_find:
                left_border = middle_border
            elif middle_border + answer_to_call_less + 2 > index_to_find:
                right_border = middle_border
            else:
                left_border = middle_border
                bool_t = True
                break
        if bool_t:
            answer_second_index = nums2[left_border]
    # print(answer_first_index, answer_second_index)
    if bool_t:
        return float((answer_first_index + answer_second_index) / 2)
    else:
        return float(answer_first_index)


# print(find_median([1], []), type(find_median([1], [])))
