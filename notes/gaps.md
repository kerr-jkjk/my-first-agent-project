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

命令行传参：

```python
parser = argparse.ArgumentParser(description="筛选CSV数据并按模型统计均值")

parser.add_argument(
    "--input-path",
    type=str,
    default="data/sample.csv",
    help="输入文件路径"
)
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
- 已知限制：列数错误记录被提前丢弃，记录序号不是原文件行号；
  数据合法范围检查还不完整。

