from pathlib import Path

from app.analysis.models import CsvRecord, Skips, Summary
from app.analysis.io import read_csv_rows, write_json
from app.analysis.validation import parse_row

# 传入合法数据，得到统计结果
def summarize_records(records: list[CsvRecord]) -> Summary:
    result = {}
    groups = {}
    for record in records:
        if record.model_name not in groups:
            groups[record.model_name] = []
        groups[record.model_name].append([record.ppl, record.iptm])

    for model_name, csv_records in groups.items():
        count = len(csv_records)

        ppl_mean = sum(csv_record[0] for csv_record in csv_records) / count
        ipTM_mean = sum(csv_record[1] for csv_record in csv_records) / count

        result[model_name] = {
            "count": count,
            "ppl_mean": ppl_mean,
            "ipTM_mean": ipTM_mean
        }

    return result
        
    
        


def analyze_csv(
    input_path: str | Path,
    ppl_threshold: float = 10.0,
    ipTM_threshold_low: float = 0.6,
    ipTM_threshold_high: float = 1.0,
) -> tuple[Summary, Skips]:
    skips = {}
    records = []
    
    header, data = read_csv_rows(input_path)

    for rows, row in enumerate(data, start=2):
        result, reason = parse_row(row, len(header))

        if result == None:
            skips["row" + str(rows)] = {"reason": reason}
            return

        if not ((row[1] <= ppl_threshold and row[1] > 0) and (row[2] >= ipTM_threshold_low and row[2] <= ipTM_threshold_high)):
            skips["row" + str(rows)] = {"reason":"跳过，不满足筛选条件或PPL非正"}
            return
       
        records.append(result)

    data = summarize_records(records=records)

    return data, skips

