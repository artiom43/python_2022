import typing as tp


from collections import deque


def traverse_dictionary_immutable(
        dct: tp.Mapping[str, tp.Any],
        prefix: str = "") -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param prefix: prefix for key used for passing total path through recursion
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    result: list[tuple[str, int]] = []
    for key in dct:
        if type(dct[key]) == int:
            result = result + [(prefix + key, dct[key])]
        else:
            result = result + traverse_dictionary_immutable(dct[key], prefix + key + ".")
    return result


def traverse_dictionary_mutable(
        dct: tp.Mapping[str, tp.Any],
        result: list[tuple[str, int]],
        prefix: str = "") -> None:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param result: list with pairs: (full key from root to leaf joined by ".", value)
    :param prefix: prefix for key used for passing total path through recursion
    :return: None
    """
    for key in dct:
        if type(dct[key]) == int:
            result.append((prefix + key, dct[key]))
        else:
            traverse_dictionary_mutable(dct[key], result,  prefix + key + ".")
    return None


def traverse_dictionary_iterative(
        dct: tp.Mapping[str, tp.Any]
        ) -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    deq = deque([(dct, str(""))])
    result = []
    while deq:
        dct_new, prefix = deq[0]
        deq.popleft()
        for key in dct_new:
            if type(dct_new[key]) == int:
                result.append((prefix + key, dct_new[key]))
            else:
                deq.append((dct_new[key], prefix + key + "."))
    return result
