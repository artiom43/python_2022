from typing import Iterable, Generator, Any
# from collections.abc import Iterable


def flat_it(sequence: Iterable[Any]) -> Generator[Any, None, None]:
    """
    :param sequence: sequence with arbitrary level of nested iterables
    :return: generator producing flatten sequence
    """
    listt = []
    answer = []
    listt.append(sequence)
    # print(sequence)
    # return
    while len(listt) != 0:
        index = listt.pop()
        # # print(index)
        # if type(index) == str and len(index) == 1:
        #     answer.append(index)
        #     continue
        if isinstance(index, Iterable) and not (type(index) == str and len(index) == 1):
            for itera in index:
                listt.append(itera)
        else:
            answer.append(index)
        # try:
        #     # yield index
        #     some_obj = iter(index)
        #     for itera in index:
        #         listt.append(itera)
        # except TypeError:
        #     answer.append(index)
    for index in reversed(answer):
        yield index
