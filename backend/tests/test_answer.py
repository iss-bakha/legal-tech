from app.schemas import Citation, LegalAnswer
from app.services import answer as answer_mod
from app.services import llm, retrieval
from app.services.retrieval import FoundArticle

ARTICLE = FoundArticle(
    id=1,
    act_title="Трудовой кодекс РК",
    number="113",
    title="Сроки выплаты заработной платы",
    text="Заработная плата выплачивается не реже одного раза в месяц...",
    source_url="https://adilet.zan.kz/",
)


def make_answer(article_id: int) -> LegalAnswer:
    return LegalAnswer(
        summary="Работодатель обязан платить зарплату ежемесячно.",
        citations=[
            Citation(
                article_id=article_id,
                act_title="Трудовой кодекс РК",
                article_number="113",
                quote="не реже одного раза в месяц",
            )
        ],
        steps=["Напишите претензию работодателю"],
        risks=["Срок обращения в суд ограничен"],
        needs_lawyer=False,
    )


def test_citations_must_be_from_search_results():
    assert answer_mod.citations_are_valid(make_answer(1), {1, 2})
    assert not answer_mod.citations_are_valid(make_answer(99), {1, 2})
    no_cites = make_answer(1).model_copy(update={"citations": []})
    assert not answer_mod.citations_are_valid(no_cites, {1})


async def test_pipeline_rejects_invented_citation(monkeypatch):
    async def fake_search(session, query, k):
        assert "990101300123" not in query  # ПДн не уходят дальше
        return [ARTICLE]

    async def fake_llm(question, articles):
        return make_answer(article_id=42)  # ссылка на статью, которой нет в выдаче

    monkeypatch.setattr(retrieval, "search_articles", fake_search)
    monkeypatch.setattr(llm, "generate_answer", fake_llm)

    res = await answer_mod.answer_question(None, "Мой ИИН 990101300123, не платят зарплату")
    assert res.status == "not_found"
    assert res.answer is None


async def test_pipeline_returns_valid_answer(monkeypatch):
    async def fake_search(session, query, k):
        return [ARTICLE]

    async def fake_llm(question, articles):
        return make_answer(article_id=1)

    monkeypatch.setattr(retrieval, "search_articles", fake_search)
    monkeypatch.setattr(llm, "generate_answer", fake_llm)

    res = await answer_mod.answer_question(None, "Не платят зарплату 2 месяца")
    assert res.status == "answered"
    assert res.answer.citations[0].article_number == "113"


async def test_no_articles_means_not_found(monkeypatch):
    async def fake_search(session, query, k):
        return []

    monkeypatch.setattr(retrieval, "search_articles", fake_search)
    res = await answer_mod.answer_question(None, "Как зарегистрировать космический корабль?")
    assert res.status == "not_found"
