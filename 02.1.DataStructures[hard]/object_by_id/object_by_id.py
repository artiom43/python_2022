import ctypes
import struct
import typing as tp
from copy import copy


LONG_LEN = 8
INT_LEN = 4
CHAR_LEN = 1

ULONG_CHAR = "L" if ctypes.sizeof(ctypes.c_ulong) == 8 else "Q"
LONG_CHAR = "l" if ctypes.sizeof(ctypes.c_long) == 8 else "q"
DICT_OF_IDS: dict[int, tp.Any] = {}


def get_object_by_id(object_id: int) -> int | float | tuple[tp.Any, ...] | list[tp.Any] | str | bool:
    """
    Restores object by id.
    :param object_id: Object Id.
    :return: An object that corresponds to object_id.
    """
    # print(object_id)
    if object_id in DICT_OF_IDS:
        # print(id(copy(DICT_OF_IDS[object_id])))
        # print(id(DICT_OF_IDS[object_id]))
        return DICT_OF_IDS[object_id]
    answer = struct.unpack("LLli", ctypes.string_at(object_id, 28))
    if answer[1] == id(int):
        number_of_bytes = abs(answer[2])
        normal_answer = struct.unpack("LLl" + "i" * number_of_bytes, ctypes.string_at(object_id, 24 +
                                                                                      number_of_bytes * 4))
        # print(normal_answer[2], normal_answer)

        number_answer = 0
        for index in range(number_of_bytes):
            number_answer += normal_answer[3 + index] * (2 ** 30) ** index
        # print(number_answer)
        if number_of_bytes == 0:
            re_an = number_answer
        else:
            re_an = number_answer * answer[2] // number_of_bytes
        DICT_OF_IDS[object_id] = re_an
        return re_an
    if answer[1] == id(bool):
        DICT_OF_IDS[object_id] = copy(answer[3])
        return answer[3]
    if answer[1] == id(float):
        normal_answer = struct.unpack("LLd", ctypes.string_at(object_id, 24))
        # print(normal_answer[2], normal_answer)
        return normal_answer[2]
    if answer[1] == id(str):
        normal_answer = struct.unpack("LLLl16s" + 's' * answer[2], ctypes.string_at(object_id, 48 + answer[2]))
        str_answer = ""
        for index in range(normal_answer[2]):
            str_answer += normal_answer[5 + index].decode()
        DICT_OF_IDS[object_id] = copy(str_answer)
        return str_answer
    if answer[1] == id(list):
        normal_answer = struct.unpack("5L", ctypes.string_at(object_id, 40))
        size_of_list = normal_answer[2]
        # link_to_data = normal_answer[3]
        list_of_links_to_elements = struct.unpack("L" * size_of_list,
                                                  ctypes.string_at(normal_answer[3], size_of_list * 8))
        answer_list: list[tp.Any] = []
        # print("sdf")
        # print(list_of_links_to_elements)
        # answer_new = []
        DICT_OF_IDS[object_id] = answer_list
        dict_of_links_to_elements = {}
        for link in list_of_links_to_elements:
            if link not in dict_of_links_to_elements:
                dict_of_links_to_elements[link] = 1
            else:
                dict_of_links_to_elements[link] += 1
        for link in list_of_links_to_elements:
            if link == object_id and dict_of_links_to_elements[link] == len(list_of_links_to_elements):
                answer_list.extend([answer_list] * len(list_of_links_to_elements))
                print("sdfsdfdf")
                DICT_OF_IDS[object_id] = copy(answer_list)
                return answer_list
            # answer_list.append(get_object_by_id(link))
            DICT_OF_IDS[object_id].append(get_object_by_id(link))
        # if answer_new != []:
        #     return answer_new
        # DICT_OF_IDS[object_id] = copy(answer_list)
        # print("sdf")
        return DICT_OF_IDS[object_id]
        # return copy(answer_list)

    if answer[1] == id(tuple):
        size_of_tuple = answer[2]
        normal_answer = struct.unpack("3L" + "L" * size_of_tuple, ctypes.string_at(object_id, 24 + 8 * size_of_tuple))
        # print("Sdf")
        list_answer = []
        for index,  link in enumerate(normal_answer[3:]):
            # print(id(get_object_by_id(link)), id(copy()))
            list_answer.append(get_object_by_id(link))
        answer_tuple = tuple(list_answer)
        DICT_OF_IDS[object_id] = copy(answer_tuple)
        return copy(answer_tuple)
    return 1
