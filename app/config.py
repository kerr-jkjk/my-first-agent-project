import os

from dotenv import load_dotenv

from pathlib import Path

load_dotenv()


APP_NAME = os.getenv("APP_NAME", "Mini Agent")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MY_API_KEY = os.getenv("MY_API_KEY")

CSV_INPUT_PATH = os.getenv("CSV_INPUT_PATH", "data/sample.csv")
CSV_PPL_THRESHOLD = float(os.getenv("CSV_PPL_THRESHOLD", "10"))

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_PATH = Path(
    os.getenv(
        "DB_PATH",
        str(PROJECT_ROOT / "data" / "papers.db")
    )
)

