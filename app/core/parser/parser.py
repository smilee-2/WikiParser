import asyncio
from pprint import pprint

from aiohttp import ClientSession
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://ru.wikipedia.org"
LINKS_DICT = dict()


async def get_dict_urls(
    session: ClientSession, url: str, start_deep: int = 0
) -> dict[str, str] | None:
    """
    Вернем словарь ссылок на статьи рекурсивно
    путь следующий: head_url -> 1 найденная href second_url -> /
    -> 1 найденная href third_url -> ... -> 1 найденная fifth_url

    :param session: ClientSession
    :param url: ссылка на статью
    :param start_deep: точка отсчета, по умолчанию 0
    :return:
    """
    if start_deep > 5:
        return LINKS_DICT
    elif start_deep < 0:
        raise "start_deep < 0"

    response = await session.get(url=url)
    soup = BeautifulSoup(await response.text(), "html.parser")

    title = soup.find(id="firstHeading")

    links = soup.find(id="bodyContent").find_all("a")
    link = None

    for l in links:
        try:
            if l["href"].find("/wiki/") == -1:
                continue
            link = l

            res = requests.get(url=BASE_URL + link.get("href"))
            if res.status_code == 200:
                break
            continue
        except KeyError:
            continue

    if link is not None:
        new_url = BASE_URL + link.get("href")
        LINKS_DICT[title.text] = new_url
        start_deep += 1
        return await get_dict_urls(session, new_url, start_deep)
    return None


async def main_parser(url: str, start_deep: int = 0):  # noqa
    async with ClientSession() as session:
        result = await get_dict_urls(session=session, url=url, start_deep=start_deep)
    pprint(result)


if __name__ == "__main__":
    url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%B0%D0%BD-%D0%A4%D1%80%D0%B0%D0%BD%D1%86%D0%B8%D1%81%D0%BA%D0%BE"
    asyncio.run(main_parser(url=url))
