import os
from bs4 import BeautifulSoup

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import aiohttp


message = 'rpo'


async def pooler(answer = None):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.google.ru/search?q={message}') as resp:
            text = await resp.text()
            print(resp)
            soup = BeautifulSoup(resp.text)
            links = []
            for link in soup.find_all('a', attrs={"class": 'result__a'}):
                links.append(str(link))
                print(str(link))

# await pool()
