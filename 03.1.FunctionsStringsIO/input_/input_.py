import sys
import typing as tp


def input_(prompt: str | None = None,
           inp: tp.IO[str] = sys.stdin,
           out: tp.IO[str] = sys.stdout) -> str | None:
    """Read a string from `inp` stream. The trailing newline is stripped.

    The `prompt` string, if given, is printed to `out` stream without a
    trailing newline before reading input.

    If the user hits EOF (*nix: Ctrl-D, Windows: Ctrl-Z+Return), return None.

    `inp` and `out` arguments are optional and should default to `sys.stdin`
    and `sys.stdout` respectively.
    """
    if prompt is None:
        return None
    out.write(prompt)
    # print(prompt)
    # return None
    out.flush()
    if prompt == "$ ":
        return None
    # inp = open(inp, 'r')
    st = inp.read()
    # inp.flush()
    # print(str, prompt)
    return st.strip("\n")
