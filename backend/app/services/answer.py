"""Конвейер ядра: маскировка → поиск → ответ LLM → проверка ссылок.

Главное правило продукта: без ссылки на найденную статью нет вывода.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.schemas import ChatResponse, LegalAnswer
from app.services import llm, retrieval
from app.services.pii import mask_pii

NOT_FOUND_MESSAGE = (
    "Не нашёл точного ответа в законодательстве РК по вашему вопросу. "
    "Рекомендуем обратиться к юристу."
)


def citations_are_valid(answer: LegalAnswer, found_ids: set[int]) -> bool:
    """Ответ без ссылок или со ссылкой на статью вне выдачи поиска не показываем."""
    if not answer.citations:
        return False
    return all(c.article_id in found_ids for c in answer.citations)


async def answer_question(session: AsyncSession, question: str) -> ChatResponse:
    masked = mask_pii(question)

    # TODO: уточняющие вопросы, определение темы, переформулировка запроса юр. терминами.
    articles = await retrieval.search_articles(session, masked.text, get_settings().retrieval_top_k)
    if not articles:
        return ChatResponse(status="not_found", message=NOT_FOUND_MESSAGE)

    try:
        answer = await llm.generate_answer(masked.text, articles)
    except llm.LLMUnavailableError:
        return ChatResponse(
            status="unavailable",
            message="Сервис временно недоступен. Попробуйте позже.",
        )

    if not citations_are_valid(answer, {a.id for a in articles}):
        return ChatResponse(status="not_found", message=NOT_FOUND_MESSAGE)

    return ChatResponse(status="answered", answer=answer)
