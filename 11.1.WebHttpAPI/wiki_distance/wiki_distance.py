from pathlib import Path
import requests
from bs4 import BeautifulSoup
# from lxml.etree import HTML

# Directory to save your .json files to
# NB: create this directory if it doesn't exist
SAVED_JSON_DIR = Path(__file__).parent / 'visited_paths'
# COUNT = 0


def distance(source_url: str, target_url: str) -> int | None:
    """Amount of wiki articles which should be visited to reach the target one
    starting from the source url. Assuming that the next article is choosing
    always as the very first link from the first article paragraph (tag <p>).
    If the article does not have any paragraph tags or any links in the first
    paragraph then the target is considered unreachable and None is returned.
    If the next link is pointing to the already visited article, it should be
    discarded in favor of the second link from this paragraph. And so on
    until the first not visited link will be found or no links left in paragraph.
    NB. The distance between neighbour articles (one is pointing out to the other)
    assumed to be equal to 1.
    :param source_url: the url of source article from wiki
    :param target_url: the url of target article from wiki
    :return: the distance calculated as described above
    """
    # print(SAVED_JSON_DIR)
    set_of_visited_links = set()
    deque_of_visited_links = [source_url]
    number_of_visited_links = -1
    while len(deque_of_visited_links) != 0:
        source_url = deque_of_visited_links[-1]
        set_of_visited_links.add(source_url)
        deque_of_visited_links = deque_of_visited_links[0:-1]
        number_of_visited_links += 1
        # print(source_url)
        if source_url == target_url:
            return number_of_visited_links
        response = requests.get(source_url, timeout=0.01)
        # print(response.text)
        soup = BeautifulSoup(response.text)
        html = soup.html
        # html = html.findAll('body')
        # head = html.find('head')
        # body = html.find('body')
        # print(html.title)
        if len(html.findAll('table')) != 0:
            html.table.decompose()
        # html = html.find('table')
        html.meta.decompose()
        ir = 0
        while ir < 100:
            ir += 1
            if len(html.findAll('tr')) != 0:
                html.tr.decompose()
        # print(html)
        # printdfsdfsdf

        paragraphs = html.findAll('p')
        # print(paragraphs[0].contents)
        # print(paragraphs[1].contents)
        paragraph = paragraphs[0]
        # print(paragraph.text)
        i = 0
        while (paragraph.contents == [] or paragraph.text == "") and len(paragraphs) > i + 1:
            paragraph = paragraphs[i + 1]
            i += 1
        # print(paragraph.text)
        # if paragraph.text.startswith("—"):
        #     print(html)
        links = paragraph.findAll('a')
        # print(links)
        # print(target_url)
        for link in reversed(links):
            # print(link)
            try:
                if not link['href'].startswith('/wiki') or ":" in link['href']:
                    continue
            except KeyError:
                continue
            if str("https://ru.wikipedia.org" + link['href']) in set_of_visited_links:
                continue
            deque_of_visited_links.append("https://ru.wikipedia.org" + link['href'])
        # if len(paragraphs) == 0:
        #     return None
        # print(paragraphs[0])
    return None
