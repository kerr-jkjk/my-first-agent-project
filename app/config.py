import os

from dotenv import load_dotenv


load_dotenv()


APP_NAME = os.getenv("APP_NAME", "Mini Agent")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MY_API_KEY = os.getenv("MY_API_KEY")

CSV_INPUT_PATH = os.getenv("CSV_INPUT_PATH", "data/sample.csv")
CSV_PPL_THRESHOLD = float(os.getenv("CSV_PPL_THRESHOLD", "10"))