

def count_util(text: str, flags: str | None = None) -> dict[str, int]:
    """
    :param text: text to count entities
    :param flags: flags in command-like format - can be:
        * -m stands for counting characters
        * -l stands for counting lines
        * -L stands for getting length of the longest line
        * -w stands for counting words
    More than one flag can be passed at the same time, for example:
        * "-l -m"
        * "-lLw"
    Ommiting flags or passing empty string is equivalent to "-mlLw"
    :return: mapping from string keys to corresponding counter, where
    keys are selected according to the received flags:
        * "chars" - amount of characters
        * "lines" - amount of lines
        * "longest_line" - the longest line length
        * "words" - amount of words
    """
    if flags is None or flags == "":
        flags = "-mlLw"
    answer_dict = {}
    if "m" in flags:
        answer_dict["chars"] = len(text)
    if "l" in flags:
        answer_dict["lines"] = len(text.split("\n")) - 1
    if "L" in flags:
        splitted_text = text.split("\n")
        answer_dict["longest_line"] = max([len(el_str) for el_str in splitted_text])
    if "w" in flags:
        answer_dict["words"] = len(text.split())
    return answer_dict
