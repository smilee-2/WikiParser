from fastapi import APIRouter, Depends

from app.api.articles.models import ArticlesModel, ArticlesModelDB
from app.core.parser.parser import main_parser
from app.core.database.crud import ArticlesCrud
from app.core.gpt.gpt import main_gpt


router = APIRouter(prefix="/api/articles", tags=["Articles"])


@router.get("/get_parse_url_and_summary")
async def get_parse_url_and_summary(
    url: ArticlesModel = Depends(), start_deep: int = 0, end_deep: int = 5
) -> dict:
    """
    Спарсит 5 статей в глубину.
    Для переданной статьи создаст резюме

    :param start_deep: не обязательный параметр, по умолчанию 0 (имеет диапазон 0 < start_deep < 5) \n
    :param end_deep: не обязательный параметр, по умолчанию 5 \n
    :param url: url ссылка на статью wiki \n
    :return: список urls и резюме на переданную статью
    """
    urls_dict = await main_parser(url=url.url, start_deep=start_deep, end_deep=end_deep)
    head_url = next(iter(urls_dict.values()), None)
    print(head_url)
    summary = await main_gpt(f"Составь резюме этой статьи {head_url}")

    for key, val in urls_dict.items():
        if summary:
            articles_model = ArticlesModelDB(
                url=head_url, name_url=val, summary=summary
            )
            await ArticlesCrud.create_articles_in_db(articles_input=articles_model)
            summary = None
        else:
            articles_model = ArticlesModelDB(
                url=key, name_url=val, summary="Not summary"
            )
            await ArticlesCrud.create_articles_in_db(articles_input=articles_model)
    return {"summary": summary, "urls": urls_dict}


@router.get("/get_summary_by_url")
async def get_summary_by_url(url: ArticlesModel = Depends()) -> dict:
    """
    Создаст резюме на переданную статью

    :param url: url ссылка на статью wiki \n
    :return: Вернет резюме на статью от нейросети
    """
    summary = await ArticlesCrud.get_summary_by_url(url=url)
    return {"msg": summary}
