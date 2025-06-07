from pydantic import BaseModel


class Base(BaseModel):
    pass


class ArticlesModel(Base):
    url: str


class ArticlesModelDB(ArticlesModel):
    name_url: str
    summary: str
