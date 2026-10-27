## day02

完成csv文件数据读取和过滤，并进行分析。

文件读取:

```pytho
# 打开文件，读取内容
with open(input_path, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader, None) # 读取表头
    data = [row for row in reader if len(row) == len(header)]   # 过滤掉不完整的行
```

解析命令行参数：

```python
parser = argparse.ArgumentParser(description="筛选CSV数据并按模型统计均值")

parser.add_argument(
    "--input-path",
    type=str,
    default="data/sample.csv",
    help="输入文件路径"
)

# 运行命令
python pratice/analyze.py --input-path data/sample2.csv
```

写文件：

```python
with open("data/result.json", "w") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
```

从模块中导入函数：

```python
from practice.analyze_csv import analyze_csv
```

### 遇到的问题与修复

1. 空字符串转换数字报 ValueError。
   修复：使用 float，并捕获转换失败，跳过当前记录。

2. 用 records[:][0] 求均值时，误把第一条记录当成整列。
   修复：遍历每条记录，分别取出 PPL 和 ipTM 后求和。

3. 跨模块调用时报 FileNotFoundError。
   定位：从 traceback 看到传入的是 data/sample.py。
   修复：改为实际文件 data/sample.csv，重新运行成功。

4. 定义 --input-path 后，函数调用仍使用固定路径。
   修复：将 args.input_path 传入 analyze_csv。

### 函数输入输出

- analyze_csv 输入：CSV 路径、PPL 上限、ipTM 下限。
- 返回：统计结果 result、跳过记录 skips。
- main 负责：解析命令行参数、调用函数、保存 JSON。

### 验证与待练习内容

- 已验证：不同阈值产生不同结果；空文件和只有表头时输出 {}；
  可以从另一个模块导入并调用函数。
- 本次在指导下完成，后续需要练习独立拆分和实现函数。
- 已知限制：



## day04

- 写了一个测试代码test_csv.py，包括两个函数，分别测试analyze_csv.py功能是否正常，第一个测试函数测试是否能处理正确数据，第二个测试函数测试是否能够正确处理无效数据
- 测试运行命令：
```bash
python -m pytest tests/test_csv.py [-v(会显示包版本)] [-q(静默输出)]
```
- 新目录安装运行成功
- set(result)的这个set函数不太理解是什么意思：就是对result这个字典进行操作，取出其中的键，返回一个集合（注意集合这种数据类型无重复元素）
```python
{} # 空字典
set() # 空集合
{"a", "b"}  # 集合
```
- tmp_path是pytest提供的临时目录，让每个测试都有独立的文件存放位置，tmp / "example.csv" 是Path对象提供的路径拼接操作
- imput_path.write_text()会创建文件
- 注意测试文件命名需要按照这个标准`test_*.py或*_test.py`,测试函数命名需要按照这个标准`test_*`。这样pytest才会发现这些测试


## day06
- return会直接返回，continue进入下一次循环
- 为什么创建 CsvRecord 时要传入转换后的变量：因为类型不一致，传入会报错
- not A and B 与 not (A and B) 有什么区别：注意运算符优先级


## 2026-10-22：校验与可诊断异常

### 1. 为什么空字段用 `if` 检查，数字转换失败用 `except ValueError`？

空字符串本身不会抛出异常，需要通过 `if` 主动判断它是否符合业务要求。

```python
if not row[1].strip():
    return None, "跳过，ppl为空"
```

`.strip()` 去掉两侧空白，因此空字符串和只有空格的字段都能被识别。

数字转换可能抛出 `ValueError`，用 `try/except` 处理：

```python
try:
    ppl = float(row[1])
except ValueError:
    return None, "跳过，ppl不是合法数字"
```

注意：`float("")` 也会抛出 `ValueError`。提前检查空值，是为了区分“字段没有填写”和“内容不能转换成数字”，提供更具体的原因。

### 2. 为什么记录文件不存在后，还要执行 `raise`？

日志只负责记录问题，不会自动停止函数或抛出异常。

```python
try:
    header, data = read_csv_rows(input_path)
except FileNotFoundError:
    logger.error("输入文件不存在：%s", input_path)
    raise
```

这里单独的 `raise` 会重新抛出当前捕获的异常，结束本次函数调用，把问题交给调用方。

调用方可以捕获异常并处理。当前命令行入口没有捕获它，所以程序会停止，不再执行后面的 JSON 导出。

不能把“文件读取失败”直接转换成空统计结果，否则调用方无法区分“分析失败”和“分析成功但没有符合条件的数据”。

### 3. 为什么 `--ppl-threshold 0` 得到 `{}` 是正常结果？

`--ppl-threshold` 设置 PPL 的最大允许值。当前筛选规则是：

```python
0 < ppl <= ppl_threshold
```

其中，严格大于 `0` 是代码中的固定条件；上限由命令行参数设置。

传入上限 `0` 后，条件变成：

```python
0 < ppl <= 0
```

没有任何数值满足这个条件，因此所有解析成功的数据都会被筛掉。

预期行为是：

- 程序正常结束。
- `result.json` 为 `{}`。
- `records.json` 保留各条数据的跳过原因。

### 本次日志调试的收获

`parse_row()` 成功时返回的 `reason` 是空字符串。如果数据随后因阈值不合格被筛掉，需要另外设置筛选原因。

将原因写进 `skips` 字典，不会自动改变变量 `reason`。日志与跳过记录应该使用同一个原因变量，保证两者一致。



## 2026-10-22：async、await、并发与超时

### 1. 协程函数、协程对象和 Task

```python
async def nested():
    return 42
```

`async def` 定义协程函数。调用 `nested()` 得到协程对象，单独调用不会自动执行函数体。

```python
task = asyncio.create_task(nested())
```

`create_task()` 将协程封装成 Task，并交给事件循环调度。当当前任务让出执行权后，新任务就有机会执行，不必等到 `await task` 才开始。

也可以直接执行协程，不需要先显式创建 Task：

```python
result = await nested()
```

### 2. await 的作用

```python
result = await task
```

- 任务未完成：当前协程暂停，事件循环可以运行其他任务。
- 任务已完成：直接取得结果。
- 任务抛出异常：异常在这个等待位置继续传播。

因此，`await` 不只是检查状态，而是等待操作完成并取得结果。

### 3. 为什么异步顺序执行仍然需要约 5 秒？

```python
await async_io("A", 2)
await async_io("B", 3)
```

A 完成后才开始调用 B，两段等待没有重叠，总耗时约为 5 秒。

并发版本：

```python
results = await asyncio.gather(
    async_io("A", 2),
    async_io("B", 3),
)
```

两项任务被并发调度，等待时间可以重叠，总耗时约为 3 秒。

`gather()` 成功返回的结果顺序与传入顺序一致，不是按完成顺序排列。

### 4. 哪个操作让当前任务暂停？

```python
await asyncio.sleep(2)
```

它挂起当前任务，让其他任务有机会运行。

```python
time.sleep(2)
```

它阻塞当前线程。在异步函数中使用它，也不会自动变成非阻塞等待。

写了 `async` 不代表自动并发，也不保证缩短耗时。执行顺序和内部操作是否阻塞同样重要。

### 5. 为什么内部看到取消，外部看到超时？

在本次 `asyncio.timeout()` 实验中：

1. 到达超时期限。
2. 超时机制向执行该操作的 Task 发出取消请求。
3. 内部等待处收到 `asyncio.CancelledError`。
4. 内部记录取消，并通过 `raise` 继续传播。
5. 退出超时上下文时，这次取消被转换成 `TimeoutError`。
6. 外层调用方捕获超时异常。

```python
try:
    async with asyncio.timeout(2):
        await async_io("B", 3)
except TimeoutError:
    print("操作超时")
```

`TimeoutError` 在超时上下文之外捕获。

超时依赖协作式取消，并非强制杀死任意代码；阻塞事件循环的操作可能导致超时不能及时触发。

### 6. gather 的异常行为

默认情况下，某项任务抛出异常，`gather()` 会将首个异常传播给调用方，但不会因此自动取消其他任务。

不能把“一项失败”理解成“其他任务必然全部取消”。

### 7. 实验记录

| 场景 | 预期结果 | 实际结果 |
|---|---|---|
| 同步顺序执行，等待 2 秒和 3 秒 | 约 5 秒 | 5 |
| 异步顺序等待，等待 2 秒和 3 秒 | 约 5 秒 | 5 |
| 异步并发执行，等待 2 秒和 3 秒 | 约 3 秒 | 3 |
| A 等待 1 秒；B 等待 3 秒、超时 2 秒 | A 完成；B 收到取消；外层收到超时 | 2 |
| 将 B 的超时改为 4 秒 | 两项成功，约 3 秒 | 3 |

### 本次纠正的理解

- `create_task()` 负责安排执行，`await task` 负责等待结果。
- 异步操作可以直接 `await`，不一定先调用 `create_task()`。
- 异步顺序等待仍然是顺序执行。
- 超时触发取消，取消传播出来后由超时上下文转换为超时异常。



## 2026-10-26：HTTP、FastAPI 路由与请求校验

### 1. 今天完成的内容

- 将论文接口整理到 `app/api/papers.py`。
- 在主应用中注册论文路由，清除重复接口。
- 使用 Pydantic 模型约定请求和响应结构。
- 通过接口调用已有的异步模拟搜索服务。
- 修复了返回语句位于循环内部的问题。

### 2. HTTP 请求中的几个概念

| 概念 | 本项目中的例子 | 含义 |
|---|---|---|
| 请求方法 | GET、POST | 表达请求操作 |
| 路径 | `/papers/search` | 确定访问哪个接口 |
| 查询参数 | `/papers?keyword=pepmlm&limit=1` | 放在 URL 中的参数 |
| 请求体 | `{"query":"pepmlm","limit":1}` | 客户端发送的数据 |
| 响应体 | 包含 `query`、`papers` 的 JSON | 服务端返回的数据 |
| 状态码 | 200、422 | 表示请求处理结果 |

本次主要关注：

- `200`：请求成功。
- `422`：请求参数或请求体没有通过校验。
- `500`：服务端执行出错，需要查看日志。

### 3. 请求模型、响应模型和路由注册

请求模型规定客户端需要提供什么：

```python
class PaperSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=200)
    limit: int = Field(default=5, ge=1, le=20)
```

- `query` 是必填字符串，长度为 1～200。
- `limit` 未提供时使用 5，允许范围是 1～20。
- `ge` 表示大于等于，`le` 表示小于等于。
- `min_length=1` 不接受空字符串，但仍允许只有空格的字符串。

接口通过以下声明使用输入和输出约定：

```python
@router.post(
    "/papers/search",
    response_model=PaperSearchResponse,
)
async def search_papers_api(request: PaperSearchRequest):
    ...
```

- `request: PaperSearchRequest`：解析并校验请求体。
- `response_model=PaperSearchResponse`：校验和整理返回结构。

路由模块负责定义接口，主应用负责注册：

```python
from app.api.papers import router as papers_router

app = FastAPI()
app.include_router(papers_router)
```

只定义路由但没有注册，主应用就无法通过它处理请求。

### 4. 一次正常 POST 的执行过程

以请求体为例：

```json
{"query": "pepmlm", "limit": 1}
```

执行过程：

1. 客户端发送 `POST /papers/search`。
2. FastAPI 根据请求方法和路径找到接口。
3. 根据 `PaperSearchRequest` 校验请求体，创建请求对象。
4. 校验通过后，执行接口函数。
5. 接口通过 `await search_papers(request.query)` 等待搜索结果。
6. 将服务返回的 `items` 转换为接口需要的 `papers`，按 `limit` 截取数量。
7. 根据响应模型校验输出，再返回 JSON 响应。

当前搜索服务使用模拟数据，没有真正检索外部论文。

`limit` 表示最多返回多少条，不保证一定返回这么多条。模拟服务只有两条论文，因此 `limit=10` 时返回两条也是正常的。

### 5. 缺少 query 时在哪里失败

请求体：

```json
{"limit": 1}
```

`query` 是必填字段，因此在请求校验阶段失败。

FastAPI 返回 `422`，错误位置指向 `body → query`。此时接口函数和搜索服务都不会执行。

需要记住：

> 先匹配接口，再校验输入；校验通过，才执行接口函数。

Swagger 页面中的 `Server response` 才是本次实际响应；下方的响应示例只是文档展示。

### 6. 本次修复：return 放在循环内部

原来的逻辑：

```python
for ...:
    papers.append(...)
    return ...
```

添加第一条论文后就会结束整个函数，所以即使请求两条，也只返回一条。只测试 `limit=1` 无法发现这个问题。

修复后的逻辑：

```python
for index, title in enumerate(
    result.items[:request.limit],
    start=1,
):
    papers.append(
        {
            "id": index,
            "title": title,
        }
    )

return {
    "query": request.query,
    "papers": papers,
}
```

循环负责收集论文，循环结束后统一返回。这里的 `id` 是演示序号，不是数据库中的永久 ID。

### 7. 验证记录

按实际结果填写：

| 验证场景 | 预期 | 实际结果 |
|---|---|---|
| GET `/health` | 200，返回正常状态 | 待填写 |
| GET `/papers?keyword=pepmlm&limit=1` | 200，参数正确回显 | 正确 |
| POST，`query=pepmlm`、`limit=2` | 200，返回两条模拟论文 | 正确 |
| POST，缺少 `query` | 422，错误指向 `query` | 正确 |
| POST，`limit=0` | 422，错误指向 `limit` | 正确 |

分别通过 `/docs` 和 curl 验证。curl 示例：

```bash
curl -i -X POST "http://127.0.0.1:8000/papers/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"pepmlm","limit":2}'
```

```bash
curl -i -X POST "http://127.0.0.1:8000/papers/search" \
  -H "Content-Type: application/json" \
  -d '{"limit":1}'
```

原有功能回归：

```bash
python -m pytest tests/ -v
```

- 实际测试数量与结果：正确。
- 数量上限改为 10 时，10 通过、11 返回 422 的实际结果：正确。
- 最终模型上限：20。




## 2026-10-27：SQLite 表与 SQL 查询

### 1. 本次完成的内容

使用 Python 自带的 `sqlite3` 操作 SQLite，完成论文表的创建、新增、查询和更新。

- 数据库文件：`data/papers.db`。
- 数据库操作模块：`app/db.py`。
- 表名：`papers`。
- 字段：`id`、`title`、`url`、`created_at`。

数据库路径根据代码文件的位置确定，避免因执行目录不同而连接到其他数据库文件。

### 2. SQL 操作与关键理解

| SQL | 作用 |
|---|---|
| `CREATE TABLE` | 创建表 |
| `INSERT INTO` | 新增记录 |
| `SELECT` | 查询记录 |
| `UPDATE` | 更新记录 |

- `execute()`：执行 SQL。
- `fetchone()`：取得一条结果，没有匹配记录时返回 `None`。
- `fetchall()`：取得全部查询结果，没有匹配记录时返回 `[]`。
- `commit()`：提交新增、更新等修改。
- `close()`：关闭数据库连接，在 `finally` 中执行。

`CREATE TABLE IF NOT EXISTS` 可以重复调用，但不会自动修改已有表的结构。

### 3. 参数化 SQL

SQL 结构与输入数据分开传递：

```python
cursor = conn.execute(
    "SELECT id, title, url, created_at FROM papers WHERE title = ?",
    (title,),
)
```

- `?` 是值的占位符。
- `(title,)` 是只有一个元素的元组，末尾逗号不能省略。
- 不使用字符串拼接或 f-string 将用户输入放进 SQL。
- 标题包含单引号时，例如 `Agent's Guide`，仍能正常保存和查询。

更新时使用 `WHERE id = ?` 限定目标记录，避免修改整张表。

### 4. 实际验证结果

按照当天指导提供的案例进行了手动验证，结果均符合预期。

| 验证内容 | 实际结果 |
|---|---|
| 查询全部论文 | 正常返回已新增的记录 |
| 按 ID 查询 | 返回对应论文 |
| 按标题查询 `Agent's Guide` | 正确返回含单引号标题的论文 |
| 更新标题后重新查询 | 读到 `PepMLM Updated` |
| 检查其他论文 | 保持原样 |
| 退出 Python 进程后重新查询 | 数据仍然保留 |

数据保留说明修改已提交到数据库文件，而不只是存在于当前进程的变量中。

### 5. 本次问题与能力状态

- 本次执行过程中遇到的问题：无。
- 完成方式：按照指导实现并验证。
- 已理解：建表、新增、查询、更新、参数绑定及提交修改的基本过程。
- 后续巩固：在后续功能中继续练习独立编写参数化 SQL。


### 算法练习：LeetCode 27 与 26

#### 1. LeetCode 27「移除元素」

- 独立尝试用时：约 30 分钟。
- 方法：左右双指针。左指针寻找需要移除的元素，右指针寻找可以保留的元素，通过交换完成整理。
- 卡点：循环结束时，指针下标不一定等于有效元素数量。
- 修复思路：指针相遇后，判断当前位置是否需要保留；需要保留则返回 `front + 1`，否则返回 `front`。空数组单独处理。
- 完成方式：自行实现主体，在提示下修复返回长度的边界问题。
- 提交结果：通过。

#### 2. LeetCode 26「删除有序数组中的重复项」

使用同向双指针，在原数组中覆盖写入去重结果：

```python
left = 0
right = 1

while right < len(nums):
    if nums[right] != nums[left]:
        left += 1
        nums[left] = nums[right]
    right += 1

return left + 1
```

指针含义：

- `left`：已保留的最后一个不同元素的位置。
- `right`：当前正在检查的元素位置。
- `nums[:left + 1]`：已经整理好的去重结果。

数组有序，相同元素相邻。因此，只需要将当前元素与最后保留的元素比较；不同就写入下一个有效位置。

例如 `[1, 1, 2, 2, 3]`，最终有效长度为 `3`，数组前三项为 `[1, 2, 3]`。有效长度之后的内容不需要清理。

- 当前代码适用于非空有序数组。
- 若需要支持空数组，应在开头增加 `if not nums: return 0`。
- 提交结果：按实际填写。

#### 3. 两道题的区别与复杂度

| 题目 | 判断依据 | 顺序要求 | 时间复杂度 | 额外空间 |
|---|---|---|---|---|
| 27 移除元素 | 是否等于 `val` | 可以改变顺序 | O(n) | O(1) |
| 26 删除重复项 | 是否与最后保留的元素相同 | 保留原有顺序 | O(n) | O(1) |

两题都需要原地修改数组，并返回有效长度，不能只计算数量而不修改数组。

本次收获：区分“下标”和“数量”，明确每个指针的含义，再判断如何移动和写入。

原定的 26 已完成代码实现，无需顺延；27 的边界处理在后续算法复习时闭卷巩固。