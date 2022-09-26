def reverse_iterative(lst: list[int]) -> list[int]:
    """
    Return reversed list. You can use only iteration
    :param lst: input list
    :return: reversed list
    """
    reversed_list = []
    for index in range(0, len(lst)):
        reversed_list.append(lst[len(lst) - index - 1])
    return reversed_list


def reverse_inplace_iterative(lst: list[int]) -> None:
    """
    Revert list inplace. You can use only iteration
    :param lst: input list
    :return: None
    """
    list_len = len(lst)
    for index in range(0, list_len//2):
        lst[index], lst[list_len - index - 1] = lst[list_len - index - 1], lst[index]
    return None


def reverse_inplace(lst: list[int]) -> None:
    """
    Revert list inplace with reverse method
    :param lst: input list
    :return: None
    """
    lst.reverse()
    return None


def reverse_reversed(lst: list[int]) -> list[int]:
    """
    Revert list with `reversed`
    :param lst: input list
    :return: reversed list
    """
    reversed_list = list(reversed(lst))
    return reversed_list


def reverse_slice(lst: list[int]) -> list[int]:
    """
    Revert list with slicing
    :param lst: input list
    :return: reversed list
    """
    return lst[::-1]
