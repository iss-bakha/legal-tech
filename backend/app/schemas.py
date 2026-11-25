from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=4000)


class Citation(BaseModel):
    """Ссылка на статью. article_id обязан быть среди найденных поиском."""

    article_id: int
    act_title: str
    article_number: str
    quote: str = Field(description="Короткая дословная цитата из статьи")


class LegalAnswer(BaseModel):
    """Фиксированная структура ответа ИИ-юриста."""

    summary: str = Field(description="Краткий вывод простым языком")
    citations: list[Citation]
    steps: list[str] = Field(description="Пошаговый план действий")
    risks: list[str] = Field(description="Предупреждения о рисках и сроках")
    needs_lawyer: bool = Field(description="Нужно ли обратиться к живому юристу")


class ChatResponse(BaseModel):
    status: str  # "answered" | "not_found" | "unavailable"
    answer: LegalAnswer | None = None
    message: str | None = None
    disclaimer: str = (
        "Это справочная информация, а не юридическая консультация. "
        "В сложной ситуации обратитесь к юристу."
    )
