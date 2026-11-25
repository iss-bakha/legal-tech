"""Доп. функция 1: «Сфоткай договор». Пока заглушка, делаем на хакатоне."""

from fastapi import APIRouter, HTTPException, UploadFile

router = APIRouter(prefix="/contracts", tags=["доп. функция: проверка договора"])

MAX_PAGES = 10


@router.post("/analyze", status_code=501)
async def analyze_contract(files: list[UploadFile]) -> None:
    if not 1 <= len(files) <= MAX_PAGES:
        raise HTTPException(422, f"Загрузите от 1 до {MAX_PAGES} страниц")
    # TODO: OCR (Claude vision) → маскировка ПДн → тип договора → пункты →
    #       чек-лист рисков → сверка со статьями → JSON-отчёт по пунктам.
    raise HTTPException(501, "Проверка договора ещё в разработке")
