def normalize_path(path: str) -> str:
    """
    :param path: unix path to normalize
    :return: normalized path
    """
    if len(path) == 0:
        return path + "."
    list_str: list[str] = path.split("/")
    index: int = -1
    answer: list[str] = []
    answer_str: str = ""
    if path[0] == "/":
        for index_1 in range(len(list_str)):
            if list_str[index_1] == "":
                continue
            if list_str[index_1] == "..":
                if index != -1:
                    answer.pop()
                    index -= 1
            elif list_str[index_1] != ".":
                answer.append(list_str[index_1])
                index += 1
        if len(answer) == 0:
            return "/"
        for el_str in answer:
            if el_str == "":
                continue
            answer_str += "/" + el_str
        # answer_str = answer_str.replace("//", "/")
        return answer_str
    else:
        count_pt: int = 0
        for index_1 in range(len(list_str)):
            if list_str[index_1] == "":
                continue
            if list_str[index_1] == "..":
                if index != -1 and answer[index] != "..":
                    answer.pop()
                    index -= 1
                else:
                    answer.append(list_str[index_1])
                    index += 1
            elif list_str[index_1] != ".":
                answer.append(list_str[index_1])
                index += 1
            else:
                count_pt += 1
        for el_str in answer:
            if el_str == "":
                continue
            answer_str += el_str + "/"
        if len(answer_str) == 0:
            answer_str = "."
        return answer_str.strip("/")
