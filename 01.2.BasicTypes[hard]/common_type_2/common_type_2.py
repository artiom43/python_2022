import typing as tp
# from typing import Union


def convert_to_common_type(data: list[tp.Any]) -> list[tp.Any]:
    """
    Takes list of multiple types' elements and convert each element to common type according to given rules
    :param data: list of multiple types' elements
    :return: list with elements converted to common type
    """
    bool_t = True
    for element in data:
        if element is not None:
            bool_t = False
    if bool_t:
        answer_str = []
        for element in data:
            answer_str.append("")
        return answer_str
    check_whether_common_type_is_bool = True
    check_that_at_least_one_is_bool = False
    for element in data:
        if element is None or element == 1 or element == 0 or element == "" or type(element) == bool:
            pass
        else:
            check_whether_common_type_is_bool = False
        if type(element) == bool:
            check_that_at_least_one_is_bool = True
    if check_whether_common_type_is_bool and check_that_at_least_one_is_bool:
        answer_bool = []
        for element in data:
            if element is None or element == "":
                answer_bool.append(False)
                continue
            answer_bool.append(bool(element))
        return answer_bool

    check_that_common_type_is_int = True
    for element in data:
        if type(element) == int or element is None or element == "":
            pass
        else:
            check_that_common_type_is_int = False
    if check_that_common_type_is_int:
        answer_int = []
        for element in data:
            if type(element) == int:
                answer_int.append(element)
            else:
                answer_int.append(int(False))
        return answer_int

    check_that_common_type_is_float = True
    for element in data:
        if element is None or type(element) == float or type(element) == int or element == "":
            pass
        else:
            check_that_common_type_is_float = False

    if check_that_common_type_is_float:
        answer_float = []
        for element in data:
            if type(element) == int or type(element) == float:
                answer_float.append(float(element))
            else:
                answer_float.append(float(False))
        return answer_float

    check_that_common_type_is_str = True
    for element in data:
        if element is None or type(element) == str:
            pass
        else:
            check_that_common_type_is_str = False

    if check_that_common_type_is_str:
        answer_str = []
        for element in data:
            if type(element) == str:
                answer_str.append(str(element))
            else:
                answer_str.append("")
        return answer_str

    answer_list: list[tp.Any] = []
    for element in data:
        if element == "" or element is None:
            answer_list.append([])
        elif type(element) == list or type(element) == tuple:
            answer_list.append(list(element))
        else:
            answer_list.append([element])
    return answer_list


print(convert_to_common_type([122334, [121223, 9389384], (123223, 4384934), None, ""]))
