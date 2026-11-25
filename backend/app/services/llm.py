"""Обёртка над Claude API. Модель возвращает ответ строго по схеме LegalAnswer."""

import anthropic

from app.config import get_settings
from app.schemas import LegalAnswer
from app.services.retrieval import FoundArticle

SYSTEM_PROMPT = """Ты ИИ-юрист для молодёжи Республики Казахстан.
Отвечай простым языком и только на основе статей НПА РК, которые даны в теге <articles>.
Не используй знания о законах из памяти. Если в статьях нет ответа, честно скажи об этом
в summary, оставь citations пустым и поставь needs_lawyer = true.
В citations указывай только article_id из <articles> и дословные короткие цитаты.
Метки вида [ИИН_1] заменяют персональные данные, не пытайся их раскрыть."""


class LLMUnavailableError(RuntimeError):
    pass


def _format_articles(articles: list[FoundArticle]) -> str:
    parts = [
        f'<article id="{a.id}" act="{a.act_title}" number="{a.number}">\n'
        f"{a.title}\n{a.text}\n</article>"
        for a in articles
    ]
    return "<articles>\n" + "\n".join(parts) + "\n</articles>"


async def generate_answer(question: str, articles: list[FoundArticle]) -> LegalAnswer:
    settings = get_settings()
    if not settings.anthropic_api_key:
        raise LLMUnavailableError("ANTHROPIC_API_KEY не задан")

    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    try:
        response = await client.beta.messages.parse(
            model=settings.llm_model,
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"{_format_articles(articles)}\n\nВопрос: {question}",
                }
            ],
            output_format=LegalAnswer,
            # Если модель откажется отвечать, API сам повторит запрос на запасной модели.
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
    except (anthropic.APIConnectionError, anthropic.RateLimitError) as e:
        raise LLMUnavailableError(str(e)) from e
    except anthropic.APIStatusError as e:
        if e.status_code >= 500:
            raise LLMUnavailableError(str(e)) from e
        raise

    if response.stop_reason == "refusal" or response.parsed_output is None:
        raise LLMUnavailableError(f"Модель не дала ответ: {response.stop_reason}")
    return response.parsed_output
