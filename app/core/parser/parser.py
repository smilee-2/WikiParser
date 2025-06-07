import asyncio
import urllib.parse

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectionError
from bs4 import BeautifulSoup

BASE_URL = "https://ru.wikipedia.org"
LINKS_DICT_V1 = dict()


async def get_dict_urls_in_deep(
    session: ClientSession, url: str, start_deep: int = 0, end_deep: int = 5
) -> dict[str, str] | None:
    """
    Вернет словарь ссылок на статьи рекурсивно в глубину
    путь следующий: head_url -> 1 найденная href second_url -> /
    -> 1 найденная href third_url -> ... -> 1 найденная fifth_url

    :param session: ClientSession
    :param url: ссылка на статью
    :param start_deep: точка начала отсчета, по умолчанию 0
    :param end_deep: точка конца отсчета, по умолчанию 5
    :return: словарь с urls
    """
    if start_deep >= end_deep:
        return LINKS_DICT_V1
    elif start_deep < 0:
        raise "start_deep < 0"

    response = await session.get(url=url)
    soup = BeautifulSoup(await response.text(), "html.parser")

    title = soup.find(id="firstHeading")

    links = soup.find(id="mw-content-text").find_all("a")
    link = None

    for l in links:
        try:
            if (
                l["href"].find("/wiki/%") == -1
                or l["href"].find("wikimedia") != -1
                or l.attrs.keys() != {"href", "title"}
            ):
                continue
            res = await session.get(url=BASE_URL + l.get("href"))
            if urllib.parse.unquote(BASE_URL + l.get("href")) in LINKS_DICT_V1.values():
                continue
            if res.status == 200:
                link = l
                break
            continue
        except KeyError:
            continue
        except AttributeError:
            continue
        except ClientConnectionError:
            continue

    if link is not None:
        new_url = BASE_URL + link.get("href")
        LINKS_DICT_V1[title.text] = url
        start_deep += 1
        return await get_dict_urls_in_deep(session, new_url, start_deep)
    return LINKS_DICT_V1


async def main_parser(url: str, start_deep: int = 0, end_deep: int = 5):  # noqa
    async with ClientSession() as session:
        result = await get_dict_urls_in_deep(
            session=session, url=url, start_deep=start_deep, end_deep=end_deep
        )
    return result


if __name__ == "__main__":
    url = "https://ru.wikipedia.org/wiki/%D0%9D%D0%B5%D0%BD%D0%B5%D1%86%D0%BA%D0%B8%D0%B9_%D1%8F%D0%B7%D1%8B%D0%BA"
    asyncio.run(main_parser(url=url))
