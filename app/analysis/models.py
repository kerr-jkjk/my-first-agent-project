from dataclasses import dataclass

@dataclass
class CsvRecord:
    model_name: str
    ppl: float
    iptm: float

# 类型别名
Summary = dict[str, dict[str, int|float]]
Skips = dict[str, dict[str,str]]