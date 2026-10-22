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