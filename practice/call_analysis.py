from practice.analyze_csv import analyze_csv

def main():
    result, skips = analyze_csv(
        input_path="data/sample.csv",
        ppl_threshold=8,
        ipTM_threshold_low=0.6,
        ipTM_threshold_high=1.0
    )

    print("统计结果：", result)
    print("跳过记录：", skips)

if __name__ == "__main__":
    main()