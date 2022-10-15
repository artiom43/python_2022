"""
Simplified VM code which works for some cases.
You need extend/rewrite code to pass all cases.
"""

import builtins
import dis
import types
import typing as tp
import operator


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
            # print(instruction.opname)
            getattr(self, instruction.opname.lower() + "_op")(instruction.argval)
            if index != self.index:
                index = self.index
            else:
                index += 1
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
        self.push(f(*arguments))

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
        self.push(self.builtins[arg])

    def load_const_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-LOAD_CONST

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L1871
        """
        self.push(arg)

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
        name = self.pop()  # the qualified name of the function (at TOS)  # noqa
        code = self.pop()  # the code associated with the function (at TOS1)

        # TODO: use arg to parse function defaults

        def f(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
            # TODO: parse input arguments using code attributes such as co_argcount

            parsed_args: dict[str, tp.Any] = {}
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

    def pop_jump_if_true_op(self, target: int) -> None:
        bool_t = self.pop()
        if bool_t:
            self.index = target//2

    def pop_jump_if_false_op(self, target: int) -> None:
        bool_t = self.pop()
        # print(bool_t)
        if not bool_t:
            self.index = target//2

    def jump_forward_op(self, target: int) -> None:
        self.index += target//2

    def jump_if_not_exc_match_op(self, target: int) -> None:
        first_value, second_value = self.popn(2)
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

    def load_assertion_error_op(self, op: tp.Any) -> None:
        self.push(AssertionError)

    def raise_varargs_op(self, argc: int) -> None:
        if argc == 0:
            raise
        elif argc == 1:
            statem = self.pop()
            raise statem
        else:
            statem1, statem = self.popn(2)
            raise statem1 from statem

    def load_fast_op(self, var_num: str) -> None:
        # print(self.locals[var_num])
        print(dis.cmp_op)
        self.push(id(self.locals[var_num]))

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
        self.push(id(element))

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
