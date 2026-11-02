# 论文 API 复现与演示

验证日期：2026-11-02。

## 1. 验证环境与结果

- 系统：macOS。
- Python：3.12。
- 使用新克隆目录、新虚拟环境。
- 依赖安装、数据库初始化和服务启动成功。
- 全部测试通过，未记录测试总数量。
- 手动 CRUD 与异常请求演示通过。
- 验证 commit：未记录，待补记。

本记录未附原始响应全文与实际演示 ID。

## 2. 新环境运行步骤

克隆项目：

```bash
git clone https://github.com/kerr-jkjk/my-first-agent-project.git
cd my-first-agent-project
```

创建并激活虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python --version
```

确认使用 Python 3.12，安装依赖并创建配置：

```bash
python -m pip install -r requirements.txt
cp .env.example .env
```

初始化数据库：

```bash
python -c "from app.db import init_db; init_db()"
```

运行测试：

```bash
python -m pytest tests/ -v
```

启动服务：

```bash
python -m uvicorn app.api_server:app --reload --port 8001
```

访问：

- 健康检查：http://127.0.0.1:8001/health
- 接口文档：http://127.0.0.1:8001/docs

按 Ctrl+C 停止服务。

以上步骤面向新数据库。已有旧表不会因为修改建表代码就自动增加字段。

## 3. 新增论文示例

以下请求用于复现演示，不是本次原始请求实录：

```json
{
  "title": "W03 Demo Paper",
  "url": "https://example.com/w03-demo",
  "source": "arxiv"
}
```

向 POST /papers 提交后，预期返回 201，并包含：

- 数据库生成的 id。
- title、url。
- 数据库生成的 created_at。
- 保存后的 source。

后续操作使用实际返回的 id。

## 4. CRUD 演示结果

本次手动演示按以下约定通过：

| 操作 | 接口 | 结果 |
|---|---|---|
| 新增论文 | POST /papers | 201，返回完整记录及 source |
| 查询单篇 | GET /papers/{paper_id} | 200，source 与新增值一致 |
| 查询列表 | GET /papers | 200，列表中包含 source |
| 更新标题 | PATCH /papers/{paper_id} | 200，标题改变，source 保留 |
| 删除论文 | DELETE /papers/{paper_id} | 200 |
| 删除后再次查询 | GET /papers/{paper_id} | 404 |

更新标题的请求示例：

```json
{
  "title": "W03 Updated Title"
}
```

## 5. 默认值与异常行为

| 场景 | 行为 |
|---|---|
| 新增时不提供 source | 使用 manual |
| source 为空字符串 | 422 |
| source 只有空白 | 422 |
| source 显式为 null | 422 |
| 查询不存在的论文 | 404 |
| 新增重复 URL | 409 |

默认值只用于未提供字段的情况，不会自动替代显式传入的无效值。

## 6. 数据与测试隔离

- 服务默认操作项目中的 data/papers.db。
- 自动化测试使用 tmp_path 中的临时数据库。
- monkeypatch 临时替换数据库路径，测试结束后恢复。
- 测试中的 SQL 真实执行，但测试数据不会出现在浏览器访问的项目数据库中。

本次验证覆盖请求校验、数据库保存、重新查询和响应返回，避免只验证新增响应的字段回显。