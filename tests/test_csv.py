import pytest

from practice.analyze_csv import analyze_csv

def test_analyze_csv_normal(tmp_path):
    # 1.准备测试数据
    input_path = tmp_path / "normal.csv"

    input_path.write_text(
        "model_name,ppl,iptm\n"
        "modelA,8,0.7\n"
        "modelA,10,0.9\n"
        "modelA,8,0.9\n"
        "modelB,6,0.6\n",
        encoding="utf-8",
    )

    # 2. 执行待测函数
    result, skips = analyze_csv(input_path,
                                ppl_threshold=10.0,
                                ipTM_threshold_low=0.6,
                                ipTM_threshold_high=0.8
                                )

    # 3.检查结果
    assert set(result) == {"modelA", "modelB"}

    assert result["modelA"]["count"] == 1
    assert result["modelA"]["mean_ppl"] == pytest.approx(8.0)
    assert result["modelA"]["mean_iptm"] == pytest.approx(0.7)

    assert result["modelB"]["count"] == 1
    assert result["modelB"]["mean_ppl"] == pytest.approx(6.0)
    assert result["modelB"]["mean_iptm"] == pytest.approx(0.6)

    assert set(skips) == {"row3", "row4"}



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

    for record in skips.values():
        assert record["reason"]






    