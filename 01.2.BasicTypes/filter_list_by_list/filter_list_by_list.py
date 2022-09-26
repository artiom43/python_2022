def filter_list_by_list(lst_a: list[int] | range, lst_b: list[int] | range) -> list[int]:
    """
    Filter first sorted list by other sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: filtered sorted list
    """
    list_answer = []
    index_a = 0
    index_b = 0
    while index_a < len(lst_a) and index_b < len(lst_b):
        if lst_a[index_a] < lst_b[index_b]:
            list_answer.append(lst_a[index_a])
            index_a += 1
        elif lst_a[index_a] > lst_b[index_b]:
            index_b += 1
        else:
            index_a += 1
    while index_a < len(lst_a):
        list_answer.append(lst_a[index_a])
        index_a += 1
    return list_answer
