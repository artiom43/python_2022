import asyncio
import multiprocessing

import aiohttp
import requests


async def async_fetch(session: aiohttp.ClientSession, url: str) -> str:
    """
    Asyncronously fetch (get-request) single url using provided session
    :param session: aiohttp session object
    :param url: target http url
    :return: fetched text
    """
    async with session.get(url) as resp:
        text = await resp.text()
        return text


async def async_requests(urls: list[str]) -> list[str]:
    """
    Concurrently fetch provided urls using aiohttp
    :param urls: list of http urls ot fetch
    :return: list of fetched texts
    """
    # print(urls)
    async with aiohttp.ClientSession() as session:
        # answer = await async_fetch(session, urls[0])
        # print(answer)
        # print(urls)
        # lst = urls
        list_of_tasks = []
        lst = urls
        for i, url in enumerate(urls):
            list_of_tasks.append(asyncio.create_task(async_fetch(session, url)))
        for i, url in enumerate(urls):
            lst[i] = await list_of_tasks[i]

        # lst = await asyncio.gather((async_fetch(session, url) for url in urls))
        return lst


def sync_fetch(session: requests.Session, url: str) -> str:
    """
    Syncronously fetch (get-request) single url using provided session
    :param session: requests session object
    :param url: target http url
    :return: fetched text
    """
    with session.get(url) as resp:
        text = resp.text
        return text


def threaded_requests(urls: list[str]) -> list[str]:
    """
    Concurrently fetch provided urls with requests in different threads
    :param urls: list of http urls ot fetch
    :return: list of fetched texts
    """
    with requests.Session() as session:
        list_of_data = [session for url in urls]
        with multiprocessing.Pool(20) as pool:
            results = pool.starmap(sync_fetch, zip(list_of_data, urls))
        return results
