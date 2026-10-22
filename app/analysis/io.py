import csv
from pathlib import Path
import json

def read_csv_rows(
    input_path: str | Path,
) -> tuple[list[str], list[list[str]]]:
    with open(input_path, mode="r", newline='', encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader, [])

        data = [row for row in reader]

    return header, data

def write_json(data:dict, output_path:str | Path) -> None:
    with open(output_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

