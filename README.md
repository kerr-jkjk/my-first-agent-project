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
```bash
pythom -m pytest tests/test_csv.py
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

