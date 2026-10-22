import pytest

from practice.analyze_csv import analyze_csv
from app.analysis.validation import parse_row

def test_analyze_csv_normal(tmp_path):
    # 1.准备测试数据
    input_path = tmp_path / "normal.csv"

    input_path.write_text(
        "model_name,ppl,iptm\n"
        "modelA,8,0.7\n"
        "modelA,10,0.8\n"
        "modelA,12,0.9\n"
        "modelB,6,0.6\n",
        encoding="utf-8",
    )

    # 2. 执行待测函数
    result, skips = analyze_csv(input_path,
                                ppl_threshold=10.0,
                                ipTM_threshold_low=0.6,
                                )

    # 3.检查结果
    assert set(result) == {"modelA", "modelB"}

    assert result["modelA"]["count"] == 2
    assert result["modelA"]["mean_ppl"] == pytest.approx(9.0)
    assert result["modelA"]["mean_iptm"] == pytest.approx(0.75)

    assert result["modelB"]["count"] == 1
    assert result["modelB"]["mean_ppl"] == pytest.approx(6.0)
    assert result["modelB"]["mean_iptm"] == pytest.approx(0.6)

    assert set(skips) == {"row4"}



def test_analyze_csv_invalid_rows(tmp_path):

    # 1.准备输入数据
    input_path = tmp_path / "invalid.csv"

    input_path.write_text(
        "model_name,ppl,iptm\n"
        "modelA,8,0.7\n"
        "modelA,,0.8\n"
        "modelB,5\n"
        "modelA,abc,0.8\n"
        "modelB,6,0.9\n",
        encoding="utf-8",
    )

    # 2.执行待测函数
    result, skips = analyze_csv(input_path)

    # 3.检查结果
    assert set(result) == {"modelA", "modelB"}

    assert result["modelA"]["count"] == 1
    assert result["modelA"]["mean_ppl"] == pytest.approx(8.0)
    assert result["modelA"]["mean_iptm"] == pytest.approx(0.7)

    assert result["modelB"]["count"] == 1
    assert result["modelB"]["mean_ppl"] == pytest.approx(6.0)
    assert result["modelB"]["mean_iptm"] == pytest.approx(0.9)

    assert set(skips) == {"row3","row4","row5"}
    assert skips["row3"]["reason"] == "跳过，ppl为空"

    for record in skips.values():
        assert record["reason"]





def test_analyze_csv_iptm_upper_bound(tmp_path):
    # 1.准备数据
    input_path = tmp_path / "upper.csv"

    input_path.write_text(
        "model_name,ppl,iptm\n"
        "modelA,8,0.7\n"
        "modelA,10,0.8\n"
        "modelA,12,0.9\n"
        "modelB,6,0.6\n",
        encoding="utf-8",
    )

    result, skips = analyze_csv(input_path, ppl_threshold=10, ipTM_threshold_low=0.6, ipTM_threshold_high=0.7)

    assert set(result) == {"modelA", "modelB"}

    assert result["modelA"]["count"] == 1
    assert result["modelA"]["mean_ppl"] == pytest.approx(8.0)
    assert result["modelA"]["mean_iptm"] == pytest.approx(0.7)

    assert result["modelB"]["count"] == 1
    assert result["modelB"]["mean_ppl"] == pytest.approx(6.0)
    assert result["modelB"]["mean_iptm"] == pytest.approx(0.6)

    assert set(skips) == {"row3", "row4"}

    for record in skips.values():
        assert record["reason"]


def test_parse_row_valid():
    record, reason = parse_row([" modelA ", "8", "0.7"], 3)

    assert record is not None
    assert reason == ""
    assert record.model_name == "modelA"
    assert isinstance(record.ppl, float)
    assert isinstance(record.iptm, float)
    assert record.ppl == pytest.approx(8.0)
    assert record.iptm == pytest.approx(0.7)

def test_analyze_csv_missing_file(tmp_path):
    input_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        analyze_csv(input_path)

def test_analyze_csv_bad_number(tmp_path):
    # 1.准备输入数据
    input_path = tmp_path / "bad.csv"

    input_path.write_text(
        "model_name,ppl,iptm\n"
        "modelA,abc,0.7\n"
        "modelB,6,0.8\n",
        encoding="utf-8",
    )
    
    result, skips = analyze_csv(input_path)
    assert set(result) == {"modelB"}
    assert result["modelB"]["count"] == 1
    assert set(skips) == {"row2"}

    assert skips["row2"]["reason"] == "跳过，ppl不是合法数字"