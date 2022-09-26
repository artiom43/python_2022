def merge_iterative(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    merged_sorted_list = []
    index_a = 0
    index_b = 0
    while index_a < len(lst_a) and index_b < len(lst_b):
        if lst_a[index_a] < lst_b[index_b]:
            merged_sorted_list.append(lst_a[index_a])
            index_a += 1
        else:
            merged_sorted_list.append(lst_b[index_b])
            index_b += 1
    while index_a < len(lst_a):
        merged_sorted_list.append(lst_a[index_a])
        index_a += 1
    while index_b < len(lst_b):
        merged_sorted_list.append(lst_b[index_b])
        index_b += 1
    return merged_sorted_list


def merge_sorted(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list using `sorted`
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    merged_sorted_list = lst_a + lst_b
    return sorted(merged_sorted_list)
