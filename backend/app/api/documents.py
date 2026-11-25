"""Доп. функция 2: генерация документов по шаблонам. Пока заглушка."""

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/documents", tags=["доп. функция: документы"])

# Шаблоны будут лежать в backend/templates/<type>/ (card.yaml + template.docx).
TEMPLATES = [
    {
        "type": "deposit_claim",
        "title": "Досудебная претензия о возврате депозита",
        "status": "planned",
    },
]


@router.get("/templates")
async def list_templates() -> list[dict[str, str]]:
    return TEMPLATES


@router.post("/{doc_type}/generate", status_code=501)
async def generate_document(doc_type: str) -> None:
    # TODO: анкета → проверка полей → текст по существу (LLM) → docxtpl → проверка → DOCX/PDF.
    raise HTTPException(501, "Генерация документов ещё в разработке")
