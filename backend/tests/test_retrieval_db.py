"""Проверка поиска на настоящей базе. Нужен Postgres из docker compose (в CI поднимается сам)."""

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import get_settings
from app.services.retrieval import search_articles


@pytest.fixture
async def session():
    from sqlalchemy.ext.asyncio import AsyncSession

    engine = create_async_engine(get_settings().database_url)
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1 FROM articles LIMIT 1"))
    except Exception:
        await engine.dispose()
        pytest.skip("База недоступна: запустите `docker compose up -d db`")
    async with AsyncSession(engine) as s:
        yield s
    await engine.dispose()


async def test_finds_demo_article_by_user_wording(session):
    found = await search_articles(
        session, "Я работаю без договора, и мне не выплатили зарплату. Что делать?", 5
    )
    assert any(a.number == "113" for a in found)


async def test_unrelated_question_finds_nothing(session):
    assert await search_articles(session, "космический корабль", 5) == []
