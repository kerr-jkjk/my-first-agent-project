# Agent Learning Roadmap

用于学习 AI Agent 开发的实践项目。

## Requirements

- Python 3.9+
- Git

## Installation

Clone repository:

```bash
git clone <repository-url>
cd my-first-agent-project
```

Create virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Copy environment configuration:

```bash
cp .env.example .env
```

Then configure required environment variables in `.env`.

## Run

```bash
python -m app.main
```

## Test

```bash
pytest
```

## Project Structure

```text
app/
├── api/          # API endpoints
├── agents/       # Agent logic
├── services/     # External services
├── tools/        # Agent tools
├── models/       # Data models
├── config.py     # Application configuration
└── main.py       # Application entry point

tests/            # Tests
data/             # Local data
scripts/          # Utility scripts
```


## 当前能力自评（2026-10-13）

### 已能完成的操作
1. 能在激活虚拟环境后启动命令行项目。
   运行 python -m app.main，看到启动日志。

2. 能检查 Python 环境和已安装依赖。
   使用 python -m pip list 查看包版本。

3. 了解整个项目的大致运行逻辑，但是对细节还不是很清楚

以上操作目前是在指导下完成，还需要练习独立重做。

### 尚需学习或确认的能力
1. 无法自己完整的写出一个独立功能，需要AI协助

2. 不能独立新增一个 FastAPI 接口。
   例子：不直接复制现有代码，自己写出参数接收和返回结果。

3. 不能独立编写测试。
   例子：为错误输入写 pytest 测试，并解释断言。