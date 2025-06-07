from sqlalchemy import select

from app.core.config.config import session_maker
from app.core.database.schemas import ArticlesSchemas
from app.api.articles.models import ArticlesModelDB, ArticlesModel


class ArticlesCrud:
    @staticmethod
    async def get_summary_by_url(url: ArticlesModel) -> str | dict[str, str]:
        async with session_maker.begin() as session:
            query = select(ArticlesSchemas).where(ArticlesSchemas.url == url.url)
            result = await session.execute(query)
            articles = result.scalar_one_or_none()
            if articles:
                return articles.summary
            return {"msg": "articles not found"}

    @staticmethod
    async def create_articles_in_db(articles_input: ArticlesModelDB) -> None:
        async with session_maker.begin() as session:
            articles = ArticlesSchemas(**articles_input.model_dump())
            session.add(articles)
