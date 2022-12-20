def get_common_type(type1: type, type2: type) -> type:
    """
    Calculate common type according to rule, that it must have the most adequate interpretation after conversion.
    Look in tests for adequacy calibration.
    :param type1: one of [bool, int, float, complex, list, range, tuple, str] types
    :param type2: one of [bool, int, float, complex, list, range, tuple, str] types
    :return: the most concrete common type, which can be used to convert both input values
    """
    list_of_types = [int, float, complex, list, tuple, str]
    list_elements_of_types = {bool: True, int: 1, float: 0.1, complex: 2j, list: [], tuple: (1, ), str: ""}
    if type1 == range:
        type1 = tuple
    if type2 == range:
        type2 = tuple
    if type1 == type2:
        return type1
    for common_type in list_of_types:
        try:
            common_type(list_elements_of_types[type1])
            common_type(list_elements_of_types[type2])
        except TypeError:
            continue
        return common_type
    dict_of_types = {(type([]), type((1,))): list, (type((1,)), type([])): list}
    if (type1, type2) in dict_of_types:
        return dict_of_types[(type1, type2)]
    return str


# print(get_common_type(tuple, int))
