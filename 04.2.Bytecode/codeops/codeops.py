import dis
import types


def count_operations(source_code: types.CodeType) -> dict[str, int]:
    """Count byte code operations in given source code.

    :param source_code: the bytecode operation names to be extracted from
    :return: operation counts
    """
    list_of_instruction = list(dis.get_instructions(source_code))
    for instr in list_of_instruction:
        # print(instr)
        pass
    # print(dis.dis(source_code))
    print(source_code)
    # print(list(dis.get_instructions(source_code, first_line=4)))
    # print(list_of_instruction[0].opname, list_of_instruction[0].argval)
    dict_of_instruction = {}
    while len(list_of_instruction) != 0:
        obt = list_of_instruction[-1]
        list_of_instruction.pop()
        # print(type(obt.argval))
        # print(obt)
        if obt.opname not in dict_of_instruction:
            dict_of_instruction[obt.opname] = 1
        else:
            dict_of_instruction[obt.opname] += 1
        if type(obt.argval) == type(source_code):
            dict = count_operations(obt.argval)
            for index in dict:
                if index not in dict_of_instruction:
                    dict_of_instruction[index] = dict[index]
                else:
                    dict_of_instruction[index] += dict[index]
    return dict_of_instruction
