"""
Simplified VM code which works for some cases.
You need extend/rewrite code to pass all cases.
"""

import builtins
import dis
import types
import typing as tp
import operator

# from types import FunctionType
from typing import Any
CO_VARARGS = 4
CO_VARKEYWORDS = 8

ERR_TOO_MANY_POS_ARGS = 'Too many positional arguments'
ERR_TOO_MANY_KW_ARGS = 'Too many keyword arguments'
ERR_MULT_VALUES_FOR_ARG = 'Multiple values for arguments'
ERR_MISSING_POS_ARGS = 'Missing positional arguments'
ERR_MISSING_KWONLY_ARGS = 'Missing keyword-only arguments'
ERR_POSONLY_PASSED_AS_KW = 'Positional-only argument passed as keyword argument'


def bind_args(func__code__: tp.Any, func__defaults__: tp.Any, func__kwdefaults__: tp.Any,
              *args: Any, **kwargs: Any) -> dict[str, Any]:
    """Bind values from `args` and `kwargs` to corresponding arguments of `func`

    :param func: function to be inspected
    :param args: positional arguments to be bound
    :param kwargs: keyword arguments to be bound
    :return: `dict[argument_name] = argument_value` if binding was successful,
             raise TypeError with one of `ERR_*` error descriptions otherwise
    """
    mask = func__code__.co_flags
    t_varargs = mask//CO_VARARGS % 2
    t_varkwargs = mask//CO_VARKEYWORDS % 2
    dict_arg = {}
    dict_arg1 = {}
    count_def = 0
    if func__defaults__ is not None:
        count_def = len(func__defaults__)
    list_def = []
    if func__defaults__ is not None:
        for index in func__defaults__:
            list_def.append(index)
    index = 0
    while index < func__code__.co_argcount and count_def - index - 1 > -1:
        str = func__code__.co_varnames[func__code__.co_argcount - index - 1]
        dict_arg[str] = list_def[count_def - index - 1]
        index += 1
    index = 0
    for index in range(func__code__.co_posonlyargcount):
        if func__code__.co_varnames[index] in kwargs and t_varkwargs == 0:
            raise TypeError(ERR_POSONLY_PASSED_AS_KW)
    while index < func__code__.co_argcount and len(args) > index:
        dict_arg[func__code__.co_varnames[index]] = args[index]
        bool_t = index >= func__code__.co_posonlyargcount
        if func__code__.co_varnames[index] in kwargs and (t_varkwargs == 0 or bool_t):
            raise TypeError(ERR_MULT_VALUES_FOR_ARG)
        index += 1
    for index in range(func__code__.co_posonlyargcount, func__code__.co_argcount):
        if func__code__.co_varnames[index] in kwargs:
            dict_arg[func__code__.co_varnames[index]] = kwargs[func__code__.co_varnames[index]]

    for index in range(func__code__.co_argcount):
        if func__code__.co_varnames[index] not in dict_arg:
            raise TypeError(ERR_MISSING_POS_ARGS)
    if func__code__.co_argcount < len(args) and t_varargs == 0:
        # print(args)
        # print(kwargs)
        # print(func__code__)
        raise TypeError(ERR_TOO_MANY_POS_ARGS)
    if t_varargs == 1:
        str = func__code__.co_varnames[func__code__.co_argcount + func__code__.co_kwonlyargcount]
        dict_arg[str] = []
        for index in range(func__code__.co_argcount, len(args)):
            dict_arg[str].append(args[index])
        dict_arg[str] = tuple(dict_arg[str])
    index = 0
    while index < func__code__.co_kwonlyargcount and func__kwdefaults__ is not None:
        str = func__code__.co_varnames[func__code__.co_argcount + func__code__.co_kwonlyargcount - index - 1]
        if str in func__kwdefaults__:
            dict_arg[str] = func__kwdefaults__[str]
        index += 1
    for index in range(func__code__.co_argcount, func__code__.co_argcount + func__code__.co_kwonlyargcount):
        if func__code__.co_varnames[index] in kwargs:
            dict_arg[func__code__.co_varnames[index]] = kwargs[func__code__.co_varnames[index]]
        elif func__code__.co_varnames[index] not in dict_arg:
            raise TypeError(ERR_MISSING_KWONLY_ARGS)
    dict_kwargs = {}
    for index in range(func__code__.co_posonlyargcount, func__code__.co_argcount):
        dict_arg1[func__code__.co_varnames[index]] = 0
    for index in range(func__code__.co_argcount, func__code__.co_argcount + func__code__.co_kwonlyargcount):
        dict_arg1[func__code__.co_varnames[index]] = 0
    for indexx in kwargs:
        if indexx not in dict_arg1:
            dict_kwargs[indexx] = kwargs[indexx]
    if t_varkwargs == 0:
        if len(dict_kwargs) != 0:
            raise TypeError(ERR_TOO_MANY_KW_ARGS)
    else:
        index_x = func__code__.co_argcount + func__code__.co_kwonlyargcount + t_varargs
        dict_arg[func__code__.co_varnames[index_x]] = dict_kwargs
    return dict_arg

# from opcode import cmp_op


class Frame:
    """
    Frame header in cpython with description
        https://github.com/python/cpython/blob/3.10/Include/frameobject.h

    Text description of frame parameters
        https://docs.python.org/3/library/inspect.html?highlight=frame#types-and-members
    """

    def __init__(self,
                 frame_code: types.CodeType,
                 frame_builtins: dict[str, tp.Any],
                 frame_globals: dict[str, tp.Any],
                 frame_locals: dict[str, tp.Any]) -> None:
        self.code = frame_code
        self.builtins = frame_builtins
        self.globals = frame_globals
        self.locals = frame_locals
        self.index: int = 0
        self.data_stack: tp.Any = []
        self.return_value = None
        self.block_stack: tp.Any = []
        self.compare_operators = [
            operator.lt,
            operator.le,
            operator.eq,
            operator.ne,
            operator.gt,
            operator.ge,
            lambda x, y: x in y,
            lambda x, y: x not in y,
            lambda x, y: x is y,
            lambda x, y: x is not y,
            lambda x, y: issubclass(x, Exception) and issubclass(x, y),
        ]

    def top(self) -> tp.Any:
        return self.data_stack[-1]

    def pop(self) -> tp.Any:
        return self.data_stack.pop()

    def push(self, *values: tp.Any) -> None:
        self.data_stack.extend(values)

    def popn(self, n: int) -> tp.Any:
        """
        Pop a number of values from the value stack.
        A list of n values is returned, the deepest value first.
        """
        if n > 0:
            returned = self.data_stack[-n:]
            self.data_stack[-n:] = []
            return returned
        else:
            return []

    def run(self) -> tp.Any:
        index = 0
        list_of_instruction = list(dis.get_instructions(self.code))
        # print(len(list_of_instruction))
        while index < len(list_of_instruction):
            instruction = list_of_instruction[index]
            self.index = index
            # if instruction.opname == "DUP_TOP":
            #     print(instruction)
            # print(self.index)
            # print(instruction.opname)
            getattr(self, instruction.opname.lower() + "_op")(instruction.argval)
            if index != self.index:
                index = self.index
                if instruction.opname == "POP_JUMP_IF_TRUE":
                    # print(self.index)
                    pass
            else:
                index += 1
            if instruction.opname == "RETURN_VALUE":
                return self.return_value
            # if instruction.opname == "POP_JUMP_IF_TRUE":
            #     print(index)
        return self.return_value

    def call_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-CALL_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#4243
        """
        arguments = self.popn(arg)
        f = self.pop()
        # print(arguments)
        # print(arg)
        if arg != 0:
            self.push(f(*arguments))
        else:
            self.push(f())

    def call_function_ex_op(self, flags: int) -> None:
        # print(flags)
        if flags % 2 == 0:
            func, args = self.popn(2)
            self.push(func(*args))
        else:
            func, args, kwargs = self.popn(3)
            # print(**kwargs)
            # a, b, c = **kwargs
            # print(a, b, c)
            self.push(func(**kwargs))

    def call_function_kw_op(self, args: int) -> None:
        tupl = self.pop()
        dict = {}
        for index in reversed(tupl):
            tos = self.pop()
            dict[index] = tos
        arg_pos = args - int(len(tupl))
        pos = self.popn(arg_pos)
        func = self.pop()
        self.push(func(*pos, **dict))

    def load_name_op(self, arg: str) -> None:
        """
        Partial realization

        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-LOAD_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L2829
        """
        # TODO: parse all scopes
        if arg in self.locals:
            self.push(self.locals[arg])
        elif arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])
        else:
            raise NameError

    def load_global_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-LOAD_GLOBAL

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L2958
        """
        # TODO: parse all scopes
        if arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])
        else:
            if len(self.block_stack) == 0:
                raise NameError
            else:
                self.push(NameError)

    def load_const_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-LOAD_CONST

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L1871
        """
        self.push(arg)

    def load_fast_op(self, var_num: str) -> None:
        # print(self.locals[var_num])
        # print(dis.cmp_op)
        # print(self.locals[var_num])
        self.push(self.locals[var_num])

    def load_assertion_error_op(self, op: tp.Any) -> None:
        self.push(AssertionError)

    def load_attr_op(self, namei: str) -> None:
        element = self.pop()
        self.push(getattr(element, namei))
        # if namei in self.locals:
        #     self.push(getattr(element, self.locals[namei]))
        # elif namei in self.globals:
        #     self.push(getattr(element, self.globals[namei]))
        # elif namei in self.builtins:
        #     self.push(getattr(element, self.builtins[namei]))
        # else:
        #     print(namei)
        #     raise NameError

    def load_method_op(self, namei: str) -> None:
        obj = self.pop()
        self.push(obj, getattr(obj, namei))

    def load_build_class_op(self, x: tp.Any) -> None:
        # print(self.builtins)
        self.push(self.builtins['__build_class__'])

    def call_method_op(self, args: int) -> None:
        list_arg = self.popn(args)
        obj, met = self.popn(2)
        self.push(met(*list_arg))

    def build_const_key_map_op(self, count: int) -> None:
        tuple_k = self.pop()
        dict_ = {}
        list_ = self.popn(count)
        iter = 0
        for index in tuple_k:
            dict_[index] = list_[iter]
            iter += 1
        # print(dict_)
        self.push(dict_)

    def map_add_op(self, i: tp.Any) -> None:
        ma, key, value = self.popn(3)
        dict.__setitem__(ma, key, value)
        self.push(dict)

    def list_extend_op(self, index: int) -> None:
        list_el, element = self.popn(2)
        # print(list_el, element)
        list.extend(list_el, element)
        # print(list_el)
        self.push(list_el)

    def list_append_op(self, index: int) -> None:
        list_el, element = self.popn(2)
        list_el.append(element)
        self.push(list_el)

    def list_to_tuple_op(self, x: tp.Any) -> None:
        list_el = self.pop()
        self.push(tuple(list_el))

    def return_value_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-RETURN_VALUE

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L2436
        """
        self.return_value = self.pop()

    def pop_top_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-POP_TOP

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L1886
        """
        self.pop()

    def pop_block_op(self, x: tp.Any) -> None:
        self.block_stack.pop()

    def make_function_op(self, arg: int) -> None:

        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-MAKE_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L4290

        Parse stack:
            https://github.com/python/cpython/blob/3.10/Objects/call.c#L612

        Call function in cpython:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L4209
        """
        func_default = None
        func_kwdefault = None
        name = self.pop()  # the qualified name of the function (at TOS)  # noqa
        code = self.pop()  # the code associated with the function (at TOS1)
        # print(bin(arg))
        # TODO: use arg to parse function defaults
        if arg/4 % 2 == 1:
            self.pop()
        if arg/8 % 2 == 1:
            self.pop()
        if arg/2 % 2 == 1:
            func_kwdefault = self.pop()
        if arg % 2 == 1:
            func_default = self.pop()

        def f(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
            # TODO: parse input arguments using code attributes such as co_argcount

            parsed_args: tp.Any = bind_args(code, func_default, func_kwdefault, *args, **kwargs)
            # print(parsed_args)
            f_locals = dict(self.locals)
            f_locals.update(parsed_args)

            frame = Frame(code, self.builtins, self.globals, f_locals)  # Run code in prepared environment
            return frame.run()

        self.push(f)

    def store_name_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-STORE_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L2758
        """
        const = self.pop()
        self.locals[arg] = const

    def store_global_op(self, arg: str) -> None:
        const = self.pop()
        self.globals[arg] = const

    def store_fast_op(self, varnum: str) -> None:
        element = self.pop()
        self.locals[varnum] = element

    def store_attr_op(self, namei: str) -> None:
        tos1, tos = self.popn(2)
        tos.c = tos1
        # print(a)
        # print(tos.namei)

    def set_update_op(self, index: int) -> None:
        set_el, element = self.popn(2)
        set.update(set_el, element)
        self.push(set_el)

    def setup_finally_op(self, delta: int) -> None:
        self.block_stack.append('try')

    def setup_annotations_op(self, x: tp.Any):
        if '__annotations__' not in self.locals:
            self.locals['__annotations__'] = {}

    def dict_update_op(self, index: int) -> None:
        set_el, element = self.popn(2)
        dict.update(set_el, element)
        self.push(set_el)

    def dict_merge_op(self, index: int) -> None:
        set_el, element = self.popn(2)
        for index in element:
            if index in set_el:
                raise Exception
        dict.update(set_el, element)
        self.push(set_el)

    def delete_name_op(self, namei: str) -> None:
        self.locals.pop(namei)

    def delete_global_op(self, namei: str) -> None:
        self.globals.pop(namei)

    def delete_fast_op(self, var_name: str) -> None:
        del self.locals[var_name]

    def delete_attr_op(self, namei: str) -> None:
        tos = self.pop()
        # print(namei)
        del tos.namei

    def delete_subscr_op(self, index: tp.Any) -> None:
        tos1, tos = self.popn(2)
        del tos1[tos]

    def format_value_op(self, flags: tp.Any) -> None:
        value = self.pop()
        # print(flags[0](value))
        if not flags[1] and flags[0] is not None:
            # print(flags)
            value = flags[0](value)
        # if (flags & 0x03) == 0x00:
        #     value = self.pop()
        #     format(value)
        #     pass
        #     self.push(value)
        # if (flags & 0x03) == 0x01:
        #     value = self.pop()
        #     value = str(value)
        #     format(value)
        #     self.push(value)
        # if (flags & 0x03) == 0x02:
        #     value = self.pop()
        #     value = repr(value)
        #     format(value)
        #     self.push(value)
        # if (flags & 0x03) == 0x03:
        #     value = self.pop()
        #     value = ascii(value)
        #     format(value)
        #     self.push(value)
        # if (flags & 0x04) == 0x04:
        # fmt_spec = self.pop()
        format(value)
        self.push(value)

    def for_iter(self, delta: int) -> None:
        tos = self.pop()
        next_ = next(tos, None)
        if next_ is None:
            self.index += delta
        else:
            self.push(tos)
            self.push(next_)

    def inplace_add_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        number1 = number2 + number1
        # print(op)
        self.push(number1)

    def binary_add_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        # print(op)
        self.push(number1 + number2)

    def inplace_power_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        number1 = number2 ** number1
        # print(op)
        self.push(number1)

    def binary_power_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        self.push(number2 ** number1)

    def inplace_multiply_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        number1 = number2 * number1
        # print(op)
        self.push(number1)

    def binary_multiply_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        self.push(number2 * number1)

    def inplace_matrix_multiply_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        number1 = number2 @ number1
        # print(op)
        self.push(number1)

    def binary_matrix_multiply_op(self, op: tp.Any) -> None:
        matrix = self.pop()
        matrix1 = self.pop()
        self.push(matrix1 @ matrix)

    def inplace_floor_divide_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        number1 = number2 // number1
        # print(op)
        self.push(number1)

    def binary_floor_divide_op(self, op: tp.Any) -> None:
        number = self.pop()
        number1 = self.pop()
        self.push(number1 // number)

    def inplace_true_divide_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        number1 = number2 / number1
        # print(op)
        self.push(number1)

    def binary_true_divide_op(self, op: tp.Any) -> None:
        number = self.pop()
        number1 = self.pop()
        self.push(number1 / number)

    def inplace_modulo_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        number1 = number2 % number1
        # print(op)
        self.push(number1)

    def binary_modulo_op(self, op: tp.Any) -> None:
        number = self.pop()
        number1 = self.pop()
        self.push(number1 % number)

    def inplace_subtract_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        number1 = number2 - number1
        # print(op)
        self.push(number1)

    def binary_subtract_op(self, op: tp.Any) -> None:
        number = self.pop()
        number1 = self.pop()
        self.push(number1 - number)

    def binary_subscr_op(self, op: tp.Any) -> None:
        number = self.pop()
        number1 = self.pop()
        self.push(number1[number])

    def inplace_lshift_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        number1 = number2 << number1
        # print(op)
        self.push(number1)

    def binary_lshift_op(self, op: tp.Any) -> None:
        number = self.pop()
        number1 = self.pop()
        self.push(number1 << number)

    def inplace_rshift_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        number1 = number2 >> number1
        # print(op)
        self.push(number1)

    def binary_rshift_op(self, op: tp.Any) -> None:
        number = self.pop()
        number1 = self.pop()
        self.push(number1 >> number)

    def inplace_and_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        number1 = number2 & number1
        # print(op)
        self.push(number1)

    def binary_and_op(self, op: tp.Any) -> None:
        number = self.pop()
        number1 = self.pop()
        self.push(number1 & number)

    def inplace_xor_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        number1 = number2 ^ number1
        # print(op)
        self.push(number1)

    def binary_xor_op(self, op: tp.Any) -> None:
        number = self.pop()
        number1 = self.pop()
        self.push(number1 ^ number)

    def inplace_or_op(self, op: tp.Any) -> None:
        number1 = self.pop()
        number2 = self.pop()
        number1 = number2 | number1
        # print(op)
        self.push(number1)

    def binary_or_op(self, op: tp.Any) -> None:
        number = self.pop()
        number1 = self.pop()
        self.push(number1 | number)

    def build_list_op(self, count: int) -> None:
        list1 = list(self.popn(count))
        self.push(list1)

    def build_tuple_op(self, count: int) -> None:
        list = tuple(self.popn(count))
        self.push(list)

    def build_set_op(self, count: int) -> None:
        list = set(self.popn(count))
        self.push(list)

    def build_map_op(self, count: int) -> None:
        list_el = self.popn(2*count)
        dict_el = {}
        for index in range(count):
            dict_el[list_el[index*2]] = list_el[index*2 + 1]
        self.push(dict_el)

    def build_string_op(self, count: int) -> None:
        list_str = self.popn(count)
        str_ans = ""
        for str_i in list_str:
            str_ans += str(str_i)
        self.push(str_ans)

    def build_slice_op(self, args: int) -> None:
        if args == 2:
            x, y = self.popn(2)
            self.push(slice(x, y))
        if args == 3:
            x, y, z = self.popn(3)
            self.push(slice(x, y, z))

    def import_from_op(self, namei: str) -> None:
        tos = self.pop()
        self.push(tos)
        self.push(getattr(tos, namei))

    def import_name_op(self, namei: str) -> None:
        level, fromlist = self.popn(2)
        self.push(__import__(namei, fromlist=fromlist, level=level))

    def import_star_op(self, x: tp.Any) -> None:
        tos = self.pop()
        for index in dir(tos):
            if not index.startswith('_'):
                self.locals[index] = getattr(tos, index)

    def store_subscr_op(self, op: tp.Any) -> None:
        x, y, z = self.popn(3)
        y[z] = x
        self.push(x)
        self.push(y)

    def compare_op_op(self, opname: str) -> None:
        first_el, second_el = self.popn(2)
        # print(dis.cmp_op)
        if opname == "==":
            self.push(first_el == second_el)
        if opname == "<":
            self.push(first_el < second_el)
        if opname == "<=":
            self.push(first_el <= second_el)
        if opname == "!=":
            self.push(first_el != second_el)
        if opname == ">":
            self.push(first_el > second_el)
        if opname == ">=":
            self.push(first_el >= second_el)

    def contains_op_op(self, invert: int) -> None:
        first_el, second_el = self.popn(2)
        if invert == 1:
            self.push(first_el not in second_el)
        else:
            self.push(first_el in second_el)
        pass

    def is_op_op(self, invert: int) -> None:
        first_el, second_el = self.popn(2)
        if invert == 1:
            self.push(first_el is not second_el)
        else:
            self.push(first_el is second_el)

    def pop_jump_if_true_op(self, target: int) -> None:
        bool_t = self.top()
        if bool_t:
            self.index = target//2
            self.pop()

    def pop_jump_if_false_op(self, target: int) -> None:
        bool_t = self.top()
        # print(bool_t)
        if not bool_t:
            self.index = target//2
            self.pop()

    def jump_forward_op(self, target: int) -> None:
        self.index = target//2

    def jump_if_not_exc_match_op(self, target: int) -> None:
        first_value, second_value = self.popn(2)
        # print("sdf")
        if first_value == second_value and isinstance(first_value, Exception):
            pass
        else:
            self.index = target//2

    def jump_if_true_or_pop_op(self, target: int) -> None:
        first_element = self.top()
        if first_element:
            self.index = target//2
        else:
            self.pop()

    def jump_if_false_or_pop_op(self, target: int) -> None:
        first_element = self.top()
        if not first_element:
            self.index = target//2
        else:
            self.pop()

    def jump_absolute_op(self, target: int) -> None:
        self.index = target//2

    def raise_varargs_op(self, argc: int) -> None:
        if argc == 0:
            raise
        elif argc == 1:
            statem = self.pop()
            raise statem
        else:
            statem1, statem = self.popn(2)
            raise statem1 from statem

    def nop_op(self, op: tp.Any) -> None:
        pass

    def rot_two_op(self, op: tp.Any) -> None:
        first_el, second_el = self.popn(2)
        self.push(second_el)
        self.push(first_el)

    def rot_three_op(self, op: tp.Any) -> None:
        first_el, second_el, third_el = self.popn(3)
        self.push(third_el)
        self.push(first_el)
        self.push(second_el)

    def rot_four_op(self, op: tp.Any) -> None:
        first_el, second_el, third_el, fourth_el = self.popn(4)
        self.push(fourth_el)
        self.push(first_el)
        self.push(second_el)
        self.push(third_el)

    def dup_top_op(self, op: tp.Any) -> None:
        element = self.top()
        self.push(element)

    def unary_positive_op(self, op: tp.Any) -> None:
        first_element = self.pop()
        first_element = +first_element
        self.push(first_element)

    def unary_negative_op(self, op: tp.Any) -> None:
        first_element = self.pop()
        first_element = -first_element
        self.push(first_element)

    def unary_not_op(self, op: tp.Any) -> None:
        first_element = self.pop()
        first_element = not first_element
        self.push(first_element)

    def unary_invert_op(self, op: tp.Any) -> None:
        first_element = self.pop()
        first_element = ~first_element
        self.push(first_element)

    def unpack_ex_op(self, counts: int) -> None:
        tos = self.pop()
        list = []
        list1 = []
        for index in range(len(tos)):
            if index + 1 < counts:
                list1.append(tos[index])
            else:
                list.append(tos[index])
        self.push(reversed(list))
        for index in reversed(list1):
            self.push(index)

    def unpack_sequence_op(self, count: int) -> None:
        tos = self.pop()
        for index in reversed(tos):
            self.push(index)

    def reraise_op(self) -> None:
        exp = self.pop()
        raise exp

    def get_iter_op(self, op: tp.Any) -> None:
        first_element = self.pop()
        first_element = iter(first_element)
        self.push(first_element)

    def get_yield_from_iter_op(self, op: tp.Any) -> None:
        first_element = self.pop()
        if isinstance(first_element,  types.GeneratorType) or isinstance(first_element, types.CoroutineType):
            self.push(first_element)
        else:
            first_element = iter(first_element)
            self.push(first_element)


class VirtualMachine:
    def run(self, code_obj: types.CodeType) -> None:
        """
        :param code_obj: code for interpreting
        """
        globals_context: dict[str, tp.Any] = {}
        frame = Frame(code_obj, builtins.globals()['__builtins__'], globals_context, globals_context)
        return frame.run()
