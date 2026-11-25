-- Схема корпуса НПА. Выполняется автоматически при первом запуске контейнера Postgres.
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS acts (
    id            SERIAL PRIMARY KEY,
    code          VARCHAR(32) UNIQUE NOT NULL,   -- короткий код, например TK_RK
    title         TEXT NOT NULL,
    source_url    TEXT NOT NULL,                 -- страница на adilet.zan.kz
    revision_date DATE                           -- дата редакции
);

CREATE TABLE IF NOT EXISTS articles (
    id          SERIAL PRIMARY KEY,
    act_id      INTEGER NOT NULL REFERENCES acts(id) ON DELETE CASCADE,
    number      VARCHAR(32) NOT NULL,            -- номер статьи: 113, 113-1
    title       TEXT NOT NULL,
    text        TEXT NOT NULL,
    topic       VARCHAR(64),                     -- labor, rent, ...
    chunk_index INTEGER NOT NULL DEFAULT 0,      -- если статья порезана на части
    embedding   vector(1024),                    -- вектор для поиска по смыслу
    -- полнотекстовый индекс по-русски, пересчитывается сам
    tsv tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('russian', coalesce(title, '')), 'A') ||
        setweight(to_tsvector('russian', coalesce(text, '')), 'B')
    ) STORED,
    UNIQUE (act_id, number, chunk_index)
);

CREATE INDEX IF NOT EXISTS articles_tsv_idx ON articles USING GIN (tsv);
CREATE INDEX IF NOT EXISTS articles_embedding_idx
    ON articles USING hnsw (embedding vector_cosine_ops);

-- Демо-данные, чтобы чат работал до появления парсера. Текст сокращён, сверить с adilet.zan.kz.
INSERT INTO acts (code, title, source_url) VALUES
    ('TK_RK', 'Трудовой кодекс Республики Казахстан', 'https://adilet.zan.kz/rus/docs/K1500000414')
ON CONFLICT (code) DO NOTHING;

INSERT INTO articles (act_id, number, title, text, topic)
SELECT id, '113', 'Порядок выплаты заработной платы',
       'Заработная плата выплачивается работнику не реже одного раза в месяц не позднее '
       'первой декады следующего месяца. (ДЕМО-ТЕКСТ, заменить парсером)', 'labor'
FROM acts WHERE code = 'TK_RK'
ON CONFLICT DO NOTHING;
