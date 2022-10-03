import typing as tp


import heapq


def merge(seq: tp.Sequence[tp.Sequence[int]]) -> list[int]:
    """
    :param seq: sequence of sorted sequences
    :return: merged sorted list
    """
    answer = []
    indexes = [0]*len(seq)
    heap_elements: list[tuple[int, int]] = []
    for index in range(len(seq)):
        if len(seq[index]) != 0:
            heapq.heappush(heap_elements, (seq[index][0], index))
    while heap_elements:
        value, index = min(heap_elements)
        heapq.heappop(heap_elements)
        answer.append(value)
        indexes[index] += 1
        if indexes[index] != len(seq[index]):
            heapq.heappush(heap_elements, (seq[index][indexes[index]], index))
    return answer
