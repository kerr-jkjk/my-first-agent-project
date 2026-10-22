# 先过滤csv中的非法数据，包括数据为空、数据为负数、数据为非数字等情况，以及数据超过合理范围的情况
# 按照model_name分组，计算各组内的ppl和ipTM均值
# 按照model_name的分组结果，输出json到data/result.json文件中

import  csv
import json
import argparse
import logging

from app.analysis.service import analyze_csv
from app.analysis.io import write_json





# def analyze_csv(input_path, ppl_threshold=10.0, ipTM_threshold_low=0.6, ipTM_threshold_high=1.0):

#     # 打开文件，读取内容
#     with open(input_path, mode='r', newline='', encoding='utf-8') as infile:
#         reader = csv.reader(infile)
#         header = next(reader, None) # 读取表头
#         # data = [row for row in reader if len(row) == len(header)]   # 过滤掉不完整的行，提前丢弃，会导致记录行号与原本行号不一致
#         data = [row for row in reader] 

#     # 设定阈值
#     # ppl_threshold = 8
#     # ipTM_threshold = 0.6


#     # 记录跳过的数据以及原因
#     skips = {}
#     # 记录当前处理数据行
#     # rows = 0
#     # print(data)
#     groups = {}

#     for rows, row in enumerate(data, start=2):
#         # rows += 1

#         if len(row) != len(header):
#             skips["row" + str(rows)] = {"reason":"跳过，列数与表头不一致"}
#             continue

#         model_name = row[0].strip()
#         if not model_name:
#             skips["row" + str(rows)] = {"reason":"跳过，模型名为空"}
#             continue

#         try:
#             ppl = float(row[1])
#             ipTM = float(row[2])
#         except ValueError:
#             skips["row" + str(rows)] = {"reason":"跳过，字段为空或格式不符"}
#             continue

#         # tag = 0
#         if (ppl <= ppl_threshold and ppl > 0) and (ipTM >= ipTM_threshold_low and ipTM <= ipTM_threshold_high):
#             # tag = 1

#             if model_name not in groups:
#                 groups[model_name] = []

#             groups[model_name].append([ppl, ipTM])
#         else:
#             skips["row" + str(rows)] = {"reason":"跳过，不满足筛选条件或PPL非正"}

#     result = {}
#     for model_name, records in groups.items():
#         count = len(records)    # 记录这个model有几组数据
#         # 单独取出每一组数据的第一个元素和第二个元素，也就是ppl和ipTM，然后求平均
#         ppl_mean = sum(record[0] for record in records) / count
#         ipTM_mean = sum(record[1] for record in records) / count

#         # print(model_name, count, ppl_mean, ipTM_mean)
#         # 准备json格式输出
#         result[model_name] = {
#             "count": count,
#             "mean_ppl": ppl_mean,
#             "mean_iptm": ipTM_mean
#         }

#     # data = json.dumps(result)
#     return result, skips


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s:%(lineno)d %(message)s",
    )

    # 下面继续保留原来的 argparse 等代码
    parser = argparse.ArgumentParser(description="筛选CSV数据并按模型统计均值")

    parser.add_argument(
        "--input-path",
        type=str,
        default="data/sample.csv",
        help="输入文件路径"
    )

    parser.add_argument(
        "--ppl-threshold",
        type=float,
        default=10.0,
        help="允许的最大PPL，默认10.0",
    )

    parser.add_argument(
        "--iptm-threshold-low",
        type=float,
        default=0.6,
        help="允许的最小ipTM，默认0.6",
    )

    parser.add_argument(
        "--iptm-threshold-high",
        type=float,
        default=1.0,
        help="允许的最大ipTM，默认1.0"
    )

    args = parser.parse_args()

    result, skips = analyze_csv(input_path=args.input_path, ppl_threshold=args.ppl_threshold, ipTM_threshold_low=args.iptm_threshold_low, ipTM_threshold_high=args.iptm_threshold_high)

    write_json(result, "data/result.json")
    write_json(skips, "data/records.json")


if __name__ == "__main__":
    main()


        




