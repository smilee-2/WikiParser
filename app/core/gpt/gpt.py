import asyncio
import os
import json

from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()


async def get_response_gtp(session: ClientSession, msg: str) -> str:
    """
    Вернет ответ от нейронки на msg
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
        result = await get_response_gtp(session=session, msg=msg)
    print(result)
    return result


if __name__ == "__main__":
    asyncio.run(main_gpt("как дела?"))
