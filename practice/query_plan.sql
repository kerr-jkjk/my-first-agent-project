CREATE TABLE papers (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_papers_url_unique
ON papers(url);

INSERT INTO papers (title, url) VALUES
    ('PepMLM', 'https://example.com/1'),
    ('Agent Basics', 'https://example.com/2'),
    ('RAG Notes', 'https://example.com/3');

-- 标题索引添加前
SELECT 'before title index' as stage;

EXPLAIN QUERY PLAN
SELECT id, title, url, created_at
FROM papers
WHERE title = 'PepMLM'
ORDER BY id;

-- 添加标题索引
CREATE INDEX id_papers_title ON papers(title);

-- 标题索引添加后
SELECT 'after title index' AS stage;

EXPLAIN QUERY PLAN
SELECT id, title, url, created_at
FROM papers
WHERE title = 'PepMLM'
ORDER BY id;

-- 对比包含匹配
SELECT 'contains filter' AS stage;

EXPLAIN QUERY PLAN
SELECT id, title, url, created_at
FROM papers
WHERE title LIKE '%Agent%'
ORDER BY id
LIMIT 10 OFFSET 0;