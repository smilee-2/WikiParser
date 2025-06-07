import asyncio
import os
import json

from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()


async def get_response_from_gtp(session: ClientSession, msg: str) -> str:
    """
    Вернет ответ от нейронки на msg
    Так как запрос идет к бесплатной версии qwen3, то это работает долго -_-

    :param session: ClientSession
    :param msg: сообщение для нейронки
    :return: ответ от нейронки
    """
    response = await session.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('API_NET')}",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "model": "qwen/qwen3-30b-a3b:free",
                "messages": [{"role": "user", "content": f"{msg}"}],
            }
        ),
    )
    if response.status == 200:
        return json.loads(await response.text())["choices"][0]["message"]["content"]
    raise "Сервер qwen/qwen3-30b-a3b:free не доступен"


async def main_gpt(msg: str) -> str:
    async with ClientSession() as session:
        result = await get_response_from_gtp(session=session, msg=msg)
    return result


if __name__ == "__main__":
    answer = asyncio.run(main_gpt("как дела?"))
    print(answer)
