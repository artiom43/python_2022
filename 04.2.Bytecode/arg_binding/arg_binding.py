from types import FunctionType
from typing import Any
CO_VARARGS = 4
CO_VARKEYWORDS = 8

ERR_TOO_MANY_POS_ARGS = 'Too many positional arguments'
ERR_TOO_MANY_KW_ARGS = 'Too many keyword arguments'
ERR_MULT_VALUES_FOR_ARG = 'Multiple values for arguments'
ERR_MISSING_POS_ARGS = 'Missing positional arguments'
ERR_MISSING_KWONLY_ARGS = 'Missing keyword-only arguments'
ERR_POSONLY_PASSED_AS_KW = 'Positional-only argument passed as keyword argument'


def bind_args(func: FunctionType, *args: Any, **kwargs: Any) -> dict[str, Any]:
    """Bind values from `args` and `kwargs` to corresponding arguments of `func`

    :param func: function to be inspected
    :param args: positional arguments to be bound
    :param kwargs: keyword arguments to be bound
    :return: `dict[argument_name] = argument_value` if binding was successful,
             raise TypeError with one of `ERR_*` error descriptions otherwise
    """
    mask = func.__code__.co_flags
    t_varargs = mask//CO_VARARGS % 2
    t_varkwargs = mask//CO_VARKEYWORDS % 2
    # print(mask//CO_VARKEYWORDS % 2)
    # print(bin(func.__code__.co_flags))
    # print(func.__code__.co_varnames)
    # print(func.__code__.co_argcount)
    # print(func.__code__.co_posonlyargcount)
    # print(func.__code__.co_kwonlyargcount)
    # print(func.__defaults__)
    # print(func.__kwdefaults__)
    # print(args)
    # print(kwargs)
    dict_arg = {}
    dict_arg1 = {}
    count_def = 0
    if func.__defaults__ is not None:
        count_def = len(func.__defaults__)
    # count_def_kwargs = 0
    # print(count_def)
    # if func.__kwdefaults__ is not None:
    #     count_def_kwargs = len(func.__kwdefaults__)
    list_def = []
    if func.__defaults__ is not None:
        for index in func.__defaults__:
            list_def.append(index)
    index = 0
    while index < func.__code__.co_argcount and count_def - index - 1 > -1:
        str = func.__code__.co_varnames[func.__code__.co_argcount - index - 1]
        dict_arg[str] = list_def[count_def - index - 1]
        index += 1
    index = 0
    for index in range(func.__code__.co_posonlyargcount):
        if func.__code__.co_varnames[index] in kwargs and t_varkwargs == 0:
            raise TypeError(ERR_POSONLY_PASSED_AS_KW)
    while index < func.__code__.co_argcount and len(args) > index:
        dict_arg[func.__code__.co_varnames[index]] = args[index]
        bool_t = index >= func.__code__.co_posonlyargcount
        if func.__code__.co_varnames[index] in kwargs and (t_varkwargs == 0 or bool_t):
            raise TypeError(ERR_MULT_VALUES_FOR_ARG)
        index += 1
    # print(dict_arg)

    for index in range(func.__code__.co_posonlyargcount, func.__code__.co_argcount):
        if func.__code__.co_varnames[index] in kwargs:
            dict_arg[func.__code__.co_varnames[index]] = kwargs[func.__code__.co_varnames[index]]

    for index in range(func.__code__.co_argcount):
        if func.__code__.co_varnames[index] not in dict_arg:
            raise TypeError(ERR_MISSING_POS_ARGS)
    if func.__code__.co_argcount < len(args) and t_varargs == 0:
        raise TypeError(ERR_TOO_MANY_POS_ARGS)
    if t_varargs == 1:
        str = func.__code__.co_varnames[func.__code__.co_argcount + func.__code__.co_kwonlyargcount]
        dict_arg[str] = []
        for index in range(func.__code__.co_argcount, len(args)):
            dict_arg[str].append(args[index])
        dict_arg[str] = tuple(dict_arg[str])

    index = 0
    while index < func.__code__.co_kwonlyargcount and func.__kwdefaults__ is not None:
        str = func.__code__.co_varnames[func.__code__.co_argcount + func.__code__.co_kwonlyargcount - index - 1]
        if str in func.__kwdefaults__:
            dict_arg[str] = func.__kwdefaults__[str]
        index += 1

    for index in range(func.__code__.co_argcount, func.__code__.co_argcount + func.__code__.co_kwonlyargcount):
        if func.__code__.co_varnames[index] in kwargs:
            dict_arg[func.__code__.co_varnames[index]] = kwargs[func.__code__.co_varnames[index]]
        elif func.__code__.co_varnames[index] not in dict_arg:
            raise TypeError(ERR_MISSING_KWONLY_ARGS)

    dict_kwargs = {}
    for index in range(func.__code__.co_posonlyargcount, func.__code__.co_argcount):
        dict_arg1[func.__code__.co_varnames[index]] = 0
    for index in range(func.__code__.co_argcount, func.__code__.co_argcount + func.__code__.co_kwonlyargcount):
        dict_arg1[func.__code__.co_varnames[index]] = 0
    for indexx in kwargs:
        if indexx not in dict_arg1:
            dict_kwargs[indexx] = kwargs[indexx]
    if t_varkwargs == 0:
        if len(dict_kwargs) != 0:
            raise TypeError(ERR_TOO_MANY_KW_ARGS)
    else:
        index_x = func.__code__.co_argcount + func.__code__.co_kwonlyargcount + t_varargs
        dict_arg[func.__code__.co_varnames[index_x]] = dict_kwargs
    return dict_arg
