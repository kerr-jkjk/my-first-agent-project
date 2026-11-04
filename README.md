# Agent Learning Roadmap

用于学习 AI Agent 开发的实践项目，当前包含 CSV 数据分析、命令行交互和 FastAPI 示例。

## Requirements

- Python 3.12
- Git

## Installation

克隆仓库：

```bash
git clone https://github.com/kerr-jkjk/my-first-agent-project.git
cd my-first-agent-project
```

创建并激活虚拟环境（macOS）：

```bash
python3 -m venv .venv
source .venv/bin/activate
python --version
```

确认 Python 版本为 3.12，再安装依赖：

```bash
python -m pip install -r requirements.txt
```

## Configuration

首次配置时，复制示例文件：

```bash
cp .env.example .env
```

如果已有 `.env`，直接编辑现有文件。

CSV 分析使用以下配置：

```dotenv
CSV_INPUT_PATH=data/sample.csv
CSV_PPL_THRESHOLD=10
```

| 配置项 | 用途 | 未设置时的默认值 |
|---|---|---|
| CSV_INPUT_PATH | 默认输入文件路径 | data/sample.csv |
| CSV_PPL_THRESHOLD | 默认 PPL 上限 | 10 |

修改 `.env` 后，重新运行程序。

显式提供命令行参数时，命令行参数优先于配置默认值。

`.env` 保存本机配置，不提交 Git；`.env.example` 提供配置示例，不包含真实密钥。

## Run

以下命令均在项目根目录执行。

### CSV 分析

使用默认配置：

```bash
python -m practice.analyze_csv
```

显式指定输入路径和筛选条件：

```bash
python -m practice.analyze_csv --input-path data/sample.csv --ppl-threshold 8 --iptm-threshold-low 0.6 --iptm-threshold-high 0.9
```

输出文件：

- `data/result.json`：按模型分组的数量、PPL 均值和 ipTM 均值。
- `data/records.json`：跳过的数据记录及原因。

每次运行会覆盖这两个输出文件。


## 数据库初始化

```bash
python -c "from app.db import init_db; init_db()"
```


### 命令行交互示例

```bash
python -m app.main
```

输入 `exit` 退出。

### FastAPI 示例

```bash
python -m uvicorn app.api_server:app --reload
```

启动后访问：

- 健康检查：http://127.0.0.1:8000/health
- 接口文档：http://127.0.0.1:8000/docs

在终端按 Ctrl+C 停止服务。

## Test

运行 CSV 相关测试：

```bash
python -m pytest tests/test_csv.py -v
```

运行 tests 目录下的全部测试：

```bash
python -m pytest tests/ -v
```

## Project Structure

| 路径 | 用途 |
|---|---|
| app/analysis/ | CSV 读取、校验、统计和导出 |
| app/api_server.py | FastAPI 入口 |
| app/services/ | 服务逻辑 |
| app/tools/ | 工具函数 |
| app/models/ | 数据对象 |
| app/config.py | 环境配置读取 |
| app/main.py | 命令行交互入口 |
| practice/ | 学习练习和 CSV 命令行入口 |
| tests/ | 自动化测试 |
| data/ | 样例数据和输出结果 |
| scripts/ | 示例脚本 |
| notes/ | 环境、卡点和学习记录 |
| weekly/ | 每周验收记录 |



## Docker 运行

需要先安装并启动 Docker Desktop。

以下首次运行命令在项目根目录执行：

```bash
# 根据 Dockerfile 构建镜像
docker build -t my-first-agent-api:w04 .

# 创建并启动名为 agent-api 的容器
# 将 Mac 本机的 8003 端口映射到容器的 8000 端口
docker run -d \
  --name agent-api \
  -p 127.0.0.1:8003:8000 \
  my-first-agent-api:w04

# 查看启动日志
docker logs agent-api

# 验证健康检查，预期返回 200 和 {"status":"ok"}
curl -i http://127.0.0.1:8003/health

# 在运行中的容器内初始化 SQLite 数据库
docker exec agent-api python -c "from app.db import init_db; init_db()"

# 查询论文列表，新数据库预期返回 200 和 []
curl -i http://127.0.0.1:8003/papers
```

接口文档：http://127.0.0.1:8003/docs

停止容器：

```bash
docker stop agent-api
```

再次启动已有容器：

```bash
docker start agent-api
```

`docker run` 创建新容器，`docker start` 启动已有容器。已有同名容器时，不要重复执行创建命令。

### 运行说明

- 容器内由 Uvicorn 在 `0.0.0.0:8000` 监听请求。
- Mac 通过 `127.0.0.1:8003` 访问容器中的服务。
- `EXPOSE 8000` 声明应用使用的端口，实际端口映射由 `docker run -p` 设置。
- 本次通过 `COPY` 将代码复制进镜像，没有绑定挂载本地源码目录。
- 修改本地代码后，需要重新构建镜像，并使用新镜像重新创建容器。
- 容器数据库位于 `/app/data/papers.db`，与 Mac 项目中的数据库独立。
- 本次未配置数据库持久化挂载；停止容器保留数据，删除容器会删除其可写层中的数据库。


## Docker Compose：数据持久化与配置

使用 Compose 管理 API 容器，通过命名卷保存 SQLite 数据，并从外部传入数据库路径。

以下命令均在项目根目录执行，需要先启动 Docker Desktop。

### 1. 配置环境变量

在本地 `.env` 中增加：

```dotenv
DOCKER_DB_PATH=/app/data/papers-persistent.db
```

已有 `.env` 时直接编辑，不要覆盖原配置。`.env.example` 中提供相同的配置示例，不填写真实密钥。

配置传递过程：

1. Compose 读取 `.env` 中的 `DOCKER_DB_PATH`。
2. 根据 compose.yaml，为容器设置环境变量 `DB_PATH`。
3. app/config.py 读取 `DB_PATH`。
4. 数据库函数使用该路径。

未设置 `DOCKER_DB_PATH` 时，Compose 使用 `/app/data/papers.db`。

直接在 Mac 上运行 Python、且未设置 `DB_PATH` 时，Python 配置使用项目中的 `data/papers.db`。

### 2. 构建与启动

```bash
# 构建镜像并在后台启动服务
docker compose up -d --build

# 查看服务状态
docker compose ps

# 查看最近的启动日志
docker compose logs --tail=50 api
```

等待服务启动完成后，初始化数据库：

```bash
docker compose exec api python -c "from app.db import init_db; init_db()"
```

查看实际数据库路径：

```bash
docker compose exec api python -c "from app import db; print(db.DB_PATH)"
```

使用上述配置时，预期输出：

```text
/app/data/papers-persistent.db
```

访问：

- 健康检查：http://127.0.0.1:8004/health
- 接口文档：http://127.0.0.1:8004/docs
- 论文列表：http://127.0.0.1:8004/papers

### 3. 数据卷与数据库位置

Compose 将命名卷 papers_data 挂载到容器的 `/app/data`：

```yaml
volumes:
  - papers_data:/app/data
```

数据库需要保存在 `/app/data` 目录内，才能使用这块卷持久化。

| 位置 | 用途 |
|---|---|
| Mac 项目目录 | 保存代码和运行配置 |
| Docker 管理的命名卷 | 保存数据库文件 |
| 容器内 `/app/data` | 访问数据卷的挂载位置 |

在 macOS 上，卷数据位于 Docker Desktop 管理的 Linux 虚拟机磁盘中，不会自动出现在本地项目的 data/ 目录。

可以在 Docker Desktop 的 Volumes 页面查看，或执行：

```bash
docker volume ls
```

实际卷名通常带有 Compose 项目前缀。

### 4. 验证持久化

通过 POST /papers 新增一条论文，记录实际返回的 ID，再查询确认。

重启服务：

```bash
docker compose restart api
```

等待服务启动完成，再次查询该 ID，预期记录仍然存在。

进一步验证删除、重建容器后数据是否保留：

```bash
docker compose down
docker compose up -d
```

等待启动完成，直接查询原 ID，不重新新增记录。预期仍能读取相同的论文。

验证时保持在同一项目目录，使用同一套 Compose 配置。

### 5. 停止与再次启动

停止并删除 Compose 管理的容器和网络，保留命名卷：

```bash
docker compose down
```

再次创建并启动：

```bash
docker compose up -d
```

不要为了日常停止服务使用 `docker compose down -v`，该选项会同时删除本配置声明的数据卷。

### 6. 配置与代码更新

- 修改 compose.yaml 或 `.env` 中的运行配置后，执行 `docker compose up -d`，让 Compose 按新配置更新容器。
- 单独执行 `docker compose restart` 不会应用新的容器环境变量。
- 修改 Python 代码后，执行 `docker compose up -d --build`，重新构建并更新容器。
- 保持数据库文件位于挂载目录中，并继续使用同一个命名卷。

### 7. 密钥与配置文件

- 实际 `.env` 不提交 Git，也不复制进镜像。
- `.env.example` 只提供配置示例。
- Compose 本次只通过 environment 显式传入 DB_PATH，不会自动将 `.env` 中全部变量传入容器。
- 日志不打印密钥、完整环境变量列表或完整配置对象。
- 数据卷用于持久化，不等于备份。