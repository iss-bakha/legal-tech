"""Таблицы корпуса НПА. Схема создаётся из db/init.sql при первом запуске Postgres."""

from datetime import date

from pgvector.sqlalchemy import Vector
from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

EMBEDDING_DIM = 1024


class Base(DeclarativeBase):
    pass


class Act(Base):
    """Нормативный правовой акт, например «Трудовой кодекс РК»."""

    __tablename__ = "acts"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True)  # короткий код: "TK_RK"
    title: Mapped[str] = mapped_column(Text)
    source_url: Mapped[str] = mapped_column(Text)  # страница на adilet.zan.kz
    revision_date: Mapped[date | None] = mapped_column(Date)  # дата редакции

    articles: Mapped[list["Article"]] = relationship(back_populates="act")


class Article(Base):
    """Статья (или пункт статьи) — единица поиска."""

    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    act_id: Mapped[int] = mapped_column(ForeignKey("acts.id", ondelete="CASCADE"))
    number: Mapped[str] = mapped_column(String(32))  # "113" или "113-1"
    title: Mapped[str] = mapped_column(Text)
    text: Mapped[str] = mapped_column(Text)
    topic: Mapped[str | None] = mapped_column(String(64))  # "labor", "rent"
    chunk_index: Mapped[int] = mapped_column(Integer, default=0)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBEDDING_DIM))

    act: Mapped[Act] = relationship(back_populates="articles")
