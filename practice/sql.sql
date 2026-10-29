-- 论文练习表
CREATE TABLE demo_papers(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);

-- 笔记练习表：paper_id表示笔记属于哪篇论文
CREATE TABLE demo_notes(
    id INTEGER PRIMARY KEY,
    paper_id INTEGER NOT NULL,
    category TEXT NOT NULL
);

INSERT INTO demo_papers(id, title) VALUES
    (1, "PepMLM"),
    (2, "Agent Basics"),
    (3, "RAG Notes");

INSERT INTO demo_notes(id, paper_id, category) VALUES
    (1, 1, "research"),
    (2, 1, "research"),
    (3, 2, "agent"),
    (4, 3, "agent");

-- GROUP BY:统计每种分类的笔记数量
SELECT category, COUNT(*) as note_count
FROM demo_notes
GROUP BY category
ORDER BY category;

-- JOIN：为每条笔记补上它所属论文的标题
SELECT p.id, p.title, n.category
FROM demo_papers AS p
JOIN demo_notes AS n ON n.paper_id = p.id
ORDER BY p.id, n.id;