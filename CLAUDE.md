# Право в кармане — ИИ-юрист

PWA для молодёжи Казахстана: ИИ-юрист отвечает простым языком строго по НПА РК — вывод, ссылки на статьи,
пошаговый план, риски. Доп. функции: «Сфоткай договор» и генерация документов по шаблонам. Подробности — в README.md.

**Общаемся по-русски**: ответы, комментарии в коде, сообщения коммитов и описания PR.

## Главное правило продукта

**Без ссылки на найденную статью НПА нет вывода.** Каждая ссылка в ответе должна быть среди статей,
которые вернул поиск. Нет статей или ссылка выдумана — пользователь видит «не нашёл точного ответа,
обратитесь к юристу». Эту проверку в коде (`backend/app/services/answer.py`) нельзя ослаблять или обходить.

## Стек

- `frontend/` — Next.js 15 (App Router, TypeScript, Tailwind), PWA. Проксирует `/api/*` на бэкенд.
- `backend/` — Python 3.12 + FastAPI, зависимости через **uv**. Маскировка ПДн (`services/pii.py`),
  поиск по НПА (`services/retrieval.py`), сборка ответа (`services/answer.py`), Claude API (`services/llm.py`).
- База — Postgres + pgvector, схема в `db/init.sql`. Поменяли схему — пересоздайте базу:
  `docker compose down -v && docker compose up -d db`.
- `docker-compose.yml` — db, backend, frontend. Ключ `ANTHROPIC_API_KEY` в `.env` (шаблон `.env.example`).

## Команды

```bash
docker compose up -d db                       # база для разработки
cd backend && uv sync && uv run uvicorn app.main:app --reload
cd frontend && npm install && npm run dev
```

Проверки перед PR (те же гоняет CI):

```bash
cd backend && uv run ruff check . && uv run ruff format --check . && uv run pytest
cd frontend && npm run lint && npm run build
```
