# Право в кармане — ИИ-юрист

Веб-приложение (PWA) для молодёжи Казахстана: ИИ-юрист отвечает простым языком строго по НПА РК,
со ссылками на статьи, пошаговым планом и рисками. Доп. функции: «Сфоткай договор» и генерация
юридических документов по шаблонам.

План проекта: [ИИ-юрист: план проекта и логика работы](https://claude.ai/artifact/JhwYt6EdRz9Y2crkTP3gx5)

## Что внутри

| Папка | Что это |
|---|---|
| `frontend/` | Next.js 15 (App Router, TypeScript, Tailwind), PWA. Страницы: чат, «Сфоткай договор», «Документы» |
| `backend/` | Python 3.12 + FastAPI. Конвейер ядра, маскировка ПДн, поиск по НПА, обёртка над Claude API |
| `db/init.sql` | Схема Postgres + pgvector: акты, статьи, полнотекстовый и векторный индексы, демо-статья |
| `docker-compose.yml` | База, бэкенд и фронтенд одной командой |
| `.github/workflows/ci.yml` | Линтеры, тесты (с настоящей базой) и сборка на каждый PR |

## Как работает чат сейчас

`POST /api/chat` → маскировка ИИН, телефонов, e-mail, карт → поиск статей в Postgres →
Claude отвечает строго по найденным статьям в структуре «вывод / ссылки / шаги / риски» →
код проверяет, что каждая ссылка есть среди найденных статей. Нет статей или ссылка выдумана:
пользователь видит «не нашёл точного ответа, обратитесь к юристу».

Фронтенд проксирует `/api/*` на бэкенд, поэтому браузер ходит только на один адрес.

## Быстрый старт (Docker)

```bash
cp .env.example .env          # впишите ANTHROPIC_API_KEY
docker compose up --build
```

- сайт: http://localhost:3000
- API и документация: http://localhost:8000/docs

Без ключа API всё запускается, но чат отвечает «сервис временно недоступен».

## Разработка без Docker

Нужны Node.js 22, Python 3.12+ и [uv](https://docs.astral.sh/uv/). Базу удобнее держать в Docker:

```bash
docker compose up -d db

cd backend
uv sync
uv run uvicorn app.main:app --reload     # http://localhost:8000

cd ../frontend
npm install
npm run dev                              # http://localhost:3000
```

Проверки перед PR:

```bash
cd backend && uv run ruff check . && uv run ruff format --check . && uv run pytest
cd frontend && npm run lint && npm run build
```

Если схема в `db/init.sql` поменялась, пересоздайте базу: `docker compose down -v && docker compose up -d db`.

## Что дальше (по плану до хакатона)

- [ ] Парсер adilet.zan.kz: ТК РК и глава ГК РК об аренде, разбивка по статьям (`acts`, `articles`)
- [ ] Эмбеддинги и гибридный поиск (слова + смысл) в `backend/app/services/retrieval.py`
- [ ] Уточняющие вопросы и определение темы в `backend/app/services/answer.py`
- [ ] Маскировка ФИО и адресов в `backend/app/services/pii.py`
- [ ] Тестовый набор из 30 вопросов юристов
- [ ] Хакатон: `/api/contracts/analyze` и `/api/documents/{type}/generate` (сейчас отвечают 501)

Демо-статья 113 ТК РК в `db/init.sql` сокращена и нужна только для проверки поиска. Её заменит парсер.
