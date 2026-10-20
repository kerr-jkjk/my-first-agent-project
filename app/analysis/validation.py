from app.analysis.models import CsvRecord, Summary

def parse_row(
    row: list[str],
    expected_columns: int,
) ->tuple[CsvRecord | None, str]:
    if len(row) != expected_columns:
        return None, "跳过，列数与表头不一致"

    model_name = row[0].strip()
    if not model_name:
        return None, "跳过，模型名为空"

    try:
        ppl = float(row[1])
        ipTM = float(row[2])
    except ValueError:
        return None, "跳过，字段为空或格式不符"

    result = CsvRecord(row[0], row[1], row[2])
    return result, ""