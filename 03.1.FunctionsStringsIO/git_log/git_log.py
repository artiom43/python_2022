import typing as tp


def reformat_git_log(inp: tp.IO[str], out: tp.IO[str]) -> None:
    """Reads git log from `inp` stream, reformats it and prints to `out` stream

    Expected input format: `<sha-1>\t<date>\t<author>\t<email>\t<message>`
    Output format: `<first 7 symbols of sha-1>.....<message>`
    """
    while True:
        input_log = inp.readline()
        if not input_log:
            break
        splitted_log = input_log.split("\t")
        # print(" ".join(splitted_log[index] for index in range(10, len(splitted_log))))
        out.write(splitted_log[0][0:7]+splitted_log[4].rjust(74, '.'))
    return None
