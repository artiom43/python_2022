def get_squares(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with squared values
    """
    squared_elements = []
    for chosen_element in elements:
        squared_elements.append(chosen_element**2)
    return squared_elements


# ====================================================================================================


def get_indices_from_one(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with indices started from 1
    """
    list_indexes = []
    for index, value in enumerate(elements):
        list_indexes.append(int(index + 1))
    return list_indexes


# ====================================================================================================


def get_max_element_index(elements: list[int]) -> int | None:
    """
    :param elements: list with integer values
    :return: index of maximum element if exists, None otherwise
    """
    max_element = max(elements, default=None)
    for index, value in enumerate(elements):
        if value == max_element:
            return index
    return None

# ====================================================================================================


def get_every_second_element(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with each second element of list
    """
    # print(elements[1::2], elements)
    return elements[1::2]


# ====================================================================================================


def get_first_three_index(elements: list[int]) -> int | None:
    """
    :param elements: list with integer values
    :return: index of first "3" in the list if exists, None otherwise
    """
    for index, value in enumerate(elements):
        if value == 3:
            return index
    return None


# ====================================================================================================


def get_last_three_index(elements: list[int]) -> int | None:
    """
    :param elements: list with integer values
    :return: index of last "3" in the list if exists, None otherwise
    """
    for index, value in enumerate(reversed(elements)):
        if value == 3:
            # print(index)
            return len(elements) - index - 1
    return None


# ====================================================================================================


def get_sum(elements: list[int]) -> int:
    """
    :param elements: list with integer values
    :return: sum of elements
    """
    return sum(elements)

# ====================================================================================================


def get_min_max(elements: list[int], default: int | None) -> tuple[int | None, int | None]:
    """
    :param elements: list with integer values
    :param default: default value to return if elements are empty
    :return: (min, max) of list elements or (default, default) if elements are empty
    """
    # if min(elements) is None:
    #     return tuple((default, default))
    # else:
    #     return tuple((min(elements), max(elements)))
    return (min(elements, default=default), max(elements, default=default))

# ====================================================================================================


def get_by_index(elements: list[int], i: int, boundary: int) -> int | None:
    """
    :param elements: list with integer values
    :param i: index of elements to check with boundary
    :param boundary: boundary for check element value
    :return: element at index `i` from `elements` if element greater then boundary and None otherwise
    """
    return answer if (answer := elements[i]) > boundary else None
