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



