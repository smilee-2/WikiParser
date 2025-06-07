from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseSchemas(DeclarativeBase): ...


class ArticlesSchemas(BaseSchemas):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_url: Mapped[str] = mapped_column(nullable=False, unique=True)
    url: Mapped[str] = mapped_column(nullable=False)
    summary: Mapped[str] = mapped_column(nullable=True)
