import heapq
import string
from collections import defaultdict
import typing as tp


def normalize(
        text: str
        ) -> str:
    """
    Removes punctuation and digits and convert to lower case
    :param text: text to normalize
    :return: normalized query
    """
    answer = text.translate(str.maketrans("", "", string.punctuation))
    answer = answer.translate(str.maketrans("", "", string.digits))
    # print(answer.lower())
    return answer.lower()


def get_words(
        query: str
        ) -> list[str]:
    """
    Split by words and leave only words with letters greater than 3
    :param query: query to split
    :return: filtered and split query by words
    """
    list_of_str = query.split()
    return [word for word in list_of_str if len(word) > 3]


def build_index(
        banners: list[str]
        ) -> dict[str, list[int]]:
    """
    Create index from words to banners ids with preserving order and without repetitions
    :param banners: list of banners for indexation
    :return: mapping from word to banners ids
    """
    dict_of_banners: dict[str, list[int]] = defaultdict(list)
    for index, string_of_word in enumerate(banners):
        list_of_words = get_words(normalize(string_of_word))
        for word in list_of_words:
            if index not in dict_of_banners[word]:
                dict_of_banners[word].append(index)
    return dict_of_banners


def merge(seq: tp.Sequence[tp.Sequence[int]]) -> list[int]:
    """
    :param seq: sequence of sorted sequences
    :return: merged sorted list
    """
    answer = []
    indexes = [0]*len(seq)
    heap_elements: list[tuple[int, int]] = []
    for index in range(len(seq)):
        if len(seq[index]) != 0:
            heapq.heappush(heap_elements, (seq[index][0], index))
    while heap_elements:
        value, index = min(heap_elements)
        heapq.heappop(heap_elements)
        answer.append(value)
        indexes[index] += 1
        if indexes[index] != len(seq[index]):
            heapq.heappush(heap_elements, (seq[index][indexes[index]], index))
    return answer


def get_banner_indices_by_query(
        query: str,
        index: dict[str, list[int]]
        ) -> list[int]:
    """
    Extract banners indices from index, if all words from query contains in indexed banner
    :param query: query to find banners
    :param index: index to search banners
    :return: list of indices of suitable banners
    """
    list_of_words = get_words(normalize(query))
    sequence_of_lists = []
    for word in list_of_words:
        sequence_of_lists.append(index[word])
    merged_list = merge(sequence_of_lists)
    answer = []
    current_number = -1
    current_cnt = 0
    print(merged_list)
    for value in merged_list:
        if value == current_number:
            current_cnt += 1
        else:
            current_number = value
            current_cnt = 1
        # print(current_number, current_cnt)
        if current_cnt >= len(list_of_words):
            answer.append(current_number)
    # print(answer, len(list_of_words))
    return answer


#########################
# Don't change this code
#########################

def get_banners(
        query: str,
        index: dict[str, list[int]],
        banners: list[str]
        ) -> list[str]:
    """
    Extract banners matched to queries
    :param query: query to match
    :param index: word-banner_ids index
    :param banners: list of banners
    :return: list of matched banners
    """
    indices = get_banner_indices_by_query(query, index)
    return [banners[i] for i in indices]

#########################
