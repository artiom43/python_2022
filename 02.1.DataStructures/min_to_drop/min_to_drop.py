import typing as tp

from collections import Counter


def get_min_to_drop(seq: tp.Sequence[tp.Any]) -> int:
    """
    :param seq: sequence of elements
    :return: number of elements need to drop to leave equal elements
    """
    seq_counter = Counter(seq)
    most_frequency = 0
    for key in seq_counter:
        most_frequency = max(most_frequency, seq_counter[key])
    return len(seq) - most_frequency
