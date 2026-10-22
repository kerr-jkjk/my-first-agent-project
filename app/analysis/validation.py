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

    ppl_str = row[1].strip()
    ipTM_str = row[2].strip()
    if not ppl_str:
        return None, "跳过，ppl为空"
    if not ipTM_str:
        return None, "跳过，ipTM为空"
    

    try:
        ppl = float(ppl_str)
    except ValueError:
        return None, "跳过，ppl不是合法数字"

    try:
        ipTM = float(ipTM_str)
    except ValueError:
        return None, "跳过，ipTM不是合法数字"

    result = CsvRecord(model_name, ppl, ipTM)
    return result, ""