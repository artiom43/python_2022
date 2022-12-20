import enum


class Status(enum.Enum):
    NEW = 0
    EXTRACTED = 1
    FINISHED = 2


def extract_alphabet(
        graph: dict[str, set[str]]
        ) -> list[str]:
    """
    Extract alphabet from graph
    :param graph: graph with partial order
    :return: alphabet
    """
    list_of_vertex = []
    used_vertex = {}

    def dfs(vertex: str) -> None:
        used_vertex[vertex] = True
        for neighbour in graph[vertex]:
            if neighbour not in used_vertex:
                dfs(neighbour)
        list_of_vertex.append(vertex)

    for vertex in graph:
        if vertex not in used_vertex:
            dfs(vertex)
    answer = []
    for vertex in reversed(list_of_vertex):
        answer.append(vertex)
    return answer


def build_graph(
        words: list[str]
        ) -> dict[str, set[str]]:
    """
    Build graph from ordered words. Graph should contain all letters from words
    :param words: ordered words
    :return: graph
    """
    graph: dict[str, set[str]] = {}
    for word in words:
        for letter in word:
            graph[letter] = set()

    for index in range(len(words) - 1):
        first_word = words[index]
        second_word = words[index + 1]
        index_of_str = 0
        while index_of_str < len(first_word) and index_of_str < len(second_word):
            if first_word[index_of_str] != second_word[index_of_str]:
                graph[first_word[index_of_str]].add(second_word[index_of_str])
                break
            index_of_str += 1
    return graph


#########################
# Don't change this code
#########################

def get_alphabet(
        words: list[str]
        ) -> list[str]:
    """
    Extract alphabet from sorted words
    :param words: sorted words
    :return: alphabet
    """
    graph = build_graph(words)
    # print(graph)
    return extract_alphabet(graph)

#########################

# print(get_alphabet(["aab", "aac", "aad"]))
