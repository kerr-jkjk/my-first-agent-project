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

