from typing import List
from typing import Union


def get_fizz_buzz(n: int) -> list[int | str]:
    """
    If value divided by 3 - "Fizz",
       value divided by 5 - "Buzz",
       value divided by 15 - "FizzBuzz",
    else - value.
    :param n: size of sequence
    :return: list of values.
    """
    fizz_buzz_list: List[Union[int, str]] = []
    # fizz_buzz_list = []
    for index in range(1, n + 1):
        fizz_buzz_list.append(int(index))
        if index % 3 == 0 and index % 5 != 0:
            fizz_buzz_list[index - 1] = "Fizz"
        if index % 3 == 0 and index % 5 == 0:
            fizz_buzz_list[index - 1] = "FizzBuzz"
        if index % 3 != 0 and index % 5 == 0:
            fizz_buzz_list[index - 1] = "Buzz"
    return fizz_buzz_list
