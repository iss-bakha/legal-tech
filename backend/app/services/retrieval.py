"""Поиск статей НПА.

Сейчас: полнотекстовый поиск Postgres (по словам, русская морфология).
TODO (следующий пункт плана): добавить поиск по смыслу через pgvector и объединить
результаты (гибридный поиск, например Reciprocal Rank Fusion).
"""

from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class FoundArticle:
    id: int
    act_title: str
    number: str
    title: str
    text: str
    source_url: str


# Вопросы пользователей длинные, поэтому слова соединяем через ИЛИ, а не И:
# статья находится, если в ней есть хотя бы одно слово, и выше те, где совпало больше.
_FTS_SQL = text(
    """
    WITH q AS (
        SELECT replace(plainto_tsquery('russian', :q)::text, '&', '|')::tsquery AS query
    )
    SELECT a.id, act.title AS act_title, a.number, a.title, a.text, act.source_url
    FROM articles a
    JOIN acts act ON act.id = a.act_id, q
    WHERE a.tsv @@ q.query
    ORDER BY ts_rank(a.tsv, q.query) DESC
    LIMIT :k
    """
)


async def search_articles(session: AsyncSession, query: str, k: int) -> list[FoundArticle]:
    rows = (await session.execute(_FTS_SQL, {"q": query, "k": k})).mappings().all()
    return [FoundArticle(**row) for row in rows]
