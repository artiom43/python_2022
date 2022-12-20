def get_common_type(type1: type, type2: type) -> type:
    """
    Calculate common type according to rule, that it must have the most adequate interpretation after conversion.
    Look in tests for adequacy calibration.
    :param type1: one of [bool, int, float, complex, list, range, tuple, str] types
    :param type2: one of [bool, int, float, complex, list, range, tuple, str] types
    :return: the most concrete common type, which can be used to convert both input values
    """
    list_of_types = [bool, int, float, complex, list, range, tuple, str]
    for common_type in list_of_types:
        if isinstance(type1, common_type):
            return common_type
    # if isinstance(list, str):
    #     print("Sdf")
    return str


# print(get_common_type(type("[1,2,3]"), type([3, 4, 5])))
