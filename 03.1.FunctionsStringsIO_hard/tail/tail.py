import io
import typing as tp
from pathlib import Path
# import io


def tail(filename: Path, lines_amount: int = 10, output: tp.IO[bytes] | None = None) -> None:
    """
    :param filename: file to read lines from (the file can be very large)
    :param lines_amount: number of lines to read
    :param output: stream to write requested amount of last lines from file
                   (if nothing specified stdout will be used)
    """

    with open(filename, 'r') as file:
        rt = file.seek(0, io.SEEK_END)
        lines = ""
        chunk_size = 100
        number_of_lines = 0
        while number_of_lines <= lines_amount and rt != 0:
            new_position = max(rt - chunk_size, 0)
            file.seek(new_position)
            lines = file.read(rt - new_position) + lines
            rt = new_position
            number_of_lines = lines.count('\n')
        # list_of_lines = [""]
        list_of_lines = lines.split('\n')
        # list_of_lines = [''].extend(list_of_lines)
        # print(list_of_lines)
        for line in list_of_lines[len(list_of_lines) - lines_amount - 1:len(list_of_lines) - 1]:
            print(line)
            line += '\n'
            if output is not None:
                output.write(line.encode())
