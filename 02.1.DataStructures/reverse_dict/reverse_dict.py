import typing as tp


def revert(dct: tp.Mapping[str, str]) -> dict[str, list[str]]:
    """
    :param dct: dictionary to revert in format {key: value}
    :return: reverted dictionary {value: [key1, key2, key3]}
    """
    reverted_dct: dict[str, list[str]] = {}
    for key in dct:
        reverted_dct[dct[key]] = []
    for key in dct:
        reverted_dct[dct[key]].append(key)
    return reverted_dct
