from pathlib import Path

from app.analysis.models import CsvRecord, Skips, Summary
from app.analysis.io import read_csv_rows, write_json
from app.analysis.validation import parse_row
import logging


import time
from uuid import uuid4

logger = logging.getLogger(__name__)

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
            "mean_ppl": ppl_mean,
            "mean_iptm": ipTM_mean
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

    request_id = uuid4().hex    #生成本次调用的标识
    started = time.perf_counter()   #计算经过时间
    status = "failed"

    try:
        #开始日志
        logger.info(
            "request_id=%s event=start input_path=%s",
            request_id,
            input_path,
        )

        header, data = read_csv_rows(input_path)
        

        for rows, row in enumerate(data, start=2):
            result, reason = parse_row(row, len(header))

            if result == None:
                skips["row" + str(rows)] = {"reason": reason}
                logger.warning(
                    "request_id=%s error_type=row_validation input_path=%s，record_no=%s，reason=%s",
                    request_id,
                    input_path,
                    rows,
                    reason,
                )
                continue

            if not ((result.ppl <= ppl_threshold and result.ppl > 0) and (result.iptm >= ipTM_threshold_low and result.iptm <= ipTM_threshold_high)):
                filter_reason = "跳过，不满足筛选条件或PPL非正"
                skips["row" + str(rows)] = {"reason":filter_reason}
                logger.warning(
                    "request_id=%s error_type=filter_condition input_path=%s，record_no=%s，reason=%s",
                    request_id,
                    input_path,
                    rows,
                    filter_reason,
                )
                continue
        
            records.append(result)

        data = summarize_records(records=records)
        status = "ok"
        return data, skips
    except FileNotFoundError:
        logger.error(
            "request_id=%s error_type=file_not_found input_path=%s",
            request_id,
            input_path,
        )
        raise
    finally:
        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info(
            "request_id=%s event=end status=%s "
            "duration_ms=%.2f kept=%s skipped=%s",
            request_id,
            status,
            elapsed_ms,
            len(records),
            len(skips),
        )

